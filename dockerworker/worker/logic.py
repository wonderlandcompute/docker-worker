import json
import os
import shutil

from . import harbor
from . import util
from dockerworker.config import config
from dockerworker.log import logger
from urllib.parse import urlparse


def create_workdir(job):
    job_workdir = os.path.join(config.WORK_DIR, str(job.id))
    if os.path.isdir(job_workdir):
        shutil.rmtree(job_workdir)

    os.mkdir(job_workdir)

    input_dir = os.path.join(job_workdir, "input")
    #input_dir = os.path.join(config.WORK_DIR, "input")
    os.makedirs(input_dir, exist_ok=True)

    output_dir = os.path.join(job_workdir, "output")
    os.makedirs(output_dir)

    return job_workdir, input_dir, output_dir


def get_input_files(job, in_dir):
    descriptor = json.loads(job.input)
    for input_file in descriptor['input']:
        uri = urlparse(input_file)
        if os.path.exists(os.path.join(in_dir, os.path.basename(uri.path))):
            logger.debug("File {} already exist !".format(uri.path))
        else:
            logger.debug("Download input {}".format(input_file))
            config.backend.copy_from_backend(input_file, in_dir)


def create_containers(job, in_dir, out_dir):
    # Add needed containers
    logger.debug("Creating containers")
    descriptor = json.loads(job.input)

    mounted_ids = []
    mounted_names = []
    needed = descriptor['container'].get('needed_containers', [])
    for i, container in enumerate(needed):
        image, volumes = container['name'], container['volumes']
        repository = image.split(":")[0]
        image_tag = ""
        if len(image.split(":")) == 2:
            image_tag = image.split(":")[1]
        assert isinstance(volumes, list)

        if not config.ONLY_LOCAL_IMAGES:
            harbor.pull_image(repository, image_tag)

        tag = "JOB-{}-CNT-{}".format(job.id, i)
        mounted_names.append(tag)

        c_id = harbor.create_container(
            image,
            volumes=volumes,
            detach=True,
            name=tag,
            mem_limit="{}m".format(descriptor['max_memoryMB']),
        )
        mounted_ids.append(c_id)

    # Execute environment container
    if not config.ONLY_LOCAL_IMAGES:
        harbor.pull_image(descriptor['container']['name'],
                          descriptor['container']['tag'])

    command = util.build_command(job)
    logger.debug('Command to execute: {}'.format(command))

    entrypoint = descriptor['container'].get('entrypoint', '')
    extra_flags = descriptor['container'].get('extra_flags', [])
    needed_volumes = descriptor['container'].get('volumes', [])
    volumes_list = util.obtain_volumes(in_dir, out_dir, needed_volumes)

    main_id = harbor.create_container(
        descriptor['container']['name'],
        working_dir=descriptor['container']['workdir'],
        command=command,
        entrypoint=entrypoint,
        volumes=volumes_list,
        detach=True,
    )

    harbor.start_container(
        main_id,
        #volumes_from=mounted_names,
        #binds=volumes_list
    )

    return mounted_ids, main_id


def write_std_output(container_id, out_dir):
    with open(os.path.join(out_dir, "stdout"), "wb") as stdout_f:
        for logline in harbor.logs(container_id, stdout=True, stderr=False, stream=True):
                stdout_f.write(logline)

    with open(os.path.join(out_dir, "stderr"), "wb") as stderr_f:
        for logline in harbor.logs(container_id, stdout=False, stderr=True, stream=True):
            stderr_f.write(logline)


def upload_output_files(out_dir, upload_uri):
    logger.debug("Upload output directory `{}` to `{}`".format(out_dir, upload_uri))
    config.backend.copy_to_backend(out_dir, upload_uri)
    return config.backend.list_uploaded(upload_uri)


def obtain_output_variables(variables, out_dir):
    ret = []
    for var in variables:
        filepath = os.path.join(out_dir, var['file'])
        with open(filepath) as fp:
            value = fp.read().strip()

        ret.append("variable:{}={}".format(var['to_variable'], value))

    return ret


def handle_output(job, out_dir):
    descriptor = json.loads(job.input)
    required_outputs = descriptor.get('required_outputs', {})
    upload_uri = required_outputs.get('output_uri', '')
    upload_uri = upload_uri.replace('$JOB_ID', str(job.id))
    uploaded_files = upload_output_files(out_dir, upload_uri)

    file_contents_variables = required_outputs.get("file_contents", [])
    variables = obtain_output_variables(file_contents_variables, out_dir)

    job.output = json.dumps(uploaded_files + variables)


def pre_remove_hook():
    logger.debug("Executing pre-remove hook: `{}`".format(config.PRE_REMOVE_HOOK))
    os.system(config.PRE_REMOVE_HOOK)


def cleanup_containers(cnt_ids):
    logger.debug("Cleaning up containers")
    for container_id in cnt_ids:
        harbor.remove(container_id, v=True, force=True)


def cleanup_dir(job_dir):
    logger.debug("Cleaning up directories")
    pre_remove_hook()
    shutil.rmtree(job_dir)
