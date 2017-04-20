import time
from marshmallow import Schema, fields

class ContainerSchema(Schema):
    workdir = fields.String()
    name = fields.String()
    cpu_needed = fields.Int()
    max_memoryMB = fields.Int()
    min_memoryMB = fields.Int()
    cmd = fields.String()

class FileContentVariableSchema(Schema):
    file = fields.String()
    to_variable = fields.String()

class RequiredOutputsSchema(Schema):
    output_uri = fields.String(required=True)
    file_contents  = fields.Nested(FileContentVariableSchema, many=True)

class JobDescriptorSchema(Schema):
    input = fields.List(fields.String())
    container = fields.Nested(ContainerSchema, required=True)
    required_outputs = fields.Nested(RequiredOutputsSchema, required=True)


descriptor_schema = JobDescriptorSchema()


def multiple_replace(text, word_dict):
    for key, value in word_dict.items():
        text = text.replace(key, str(value))
    return text


def build_command(job):
    command = job.descriptor['container']['cmd']
    command = multiple_replace(command, {
        "$OUTPUT_DIR": "/output",
        "$INPUT_DIR": "/input",
        "$JOB_ID": job.job_id,
        "$TIMESTAMP": time.time()
    })

    return command


def descriptor_correct(job):
    errors = descriptor_schema.validate(job.descriptor)
    assert not errors, "Descriptor incorrect: " + str(errors)


def obtain_volumes(in_dir, out_dir, volumes):
    volumes_list = [
        "{}:/input".format(in_dir),
        "{}:/output".format(out_dir),
    ]

    volumes_list += volumes

    return volumes_list
