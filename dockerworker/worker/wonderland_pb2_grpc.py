# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from wonderlandClient import wonderland_pb2 as wonderland__pb2


class WonderlandStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CreateJob = channel.unary_unary(
        '/Wonderland/CreateJob',
        request_serializer=wonderland__pb2.Job.SerializeToString,
        response_deserializer=wonderland__pb2.Job.FromString,
        )
    self.GetJob = channel.unary_unary(
        '/Wonderland/GetJob',
        request_serializer=wonderland__pb2.RequestWithId.SerializeToString,
        response_deserializer=wonderland__pb2.Job.FromString,
        )
    self.ListJobs = channel.unary_unary(
        '/Wonderland/ListJobs',
        request_serializer=wonderland__pb2.ListJobsRequest.SerializeToString,
        response_deserializer=wonderland__pb2.ListOfJobs.FromString,
        )
    self.ModifyJob = channel.unary_unary(
        '/Wonderland/ModifyJob',
        request_serializer=wonderland__pb2.Job.SerializeToString,
        response_deserializer=wonderland__pb2.Job.FromString,
        )
    self.PullPendingJobs = channel.unary_unary(
        '/Wonderland/PullPendingJobs',
        request_serializer=wonderland__pb2.ListJobsRequest.SerializeToString,
        response_deserializer=wonderland__pb2.ListOfJobs.FromString,
        )
    self.DeleteJob = channel.unary_unary(
        '/Wonderland/DeleteJob',
        request_serializer=wonderland__pb2.RequestWithId.SerializeToString,
        response_deserializer=wonderland__pb2.Job.FromString,
        )


class WonderlandServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def CreateJob(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetJob(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListJobs(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ModifyJob(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def PullPendingJobs(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteJob(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_WonderlandServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CreateJob': grpc.unary_unary_rpc_method_handler(
          servicer.CreateJob,
          request_deserializer=wonderland__pb2.Job.FromString,
          response_serializer=wonderland__pb2.Job.SerializeToString,
      ),
      'GetJob': grpc.unary_unary_rpc_method_handler(
          servicer.GetJob,
          request_deserializer=wonderland__pb2.RequestWithId.FromString,
          response_serializer=wonderland__pb2.Job.SerializeToString,
      ),
      'ListJobs': grpc.unary_unary_rpc_method_handler(
          servicer.ListJobs,
          request_deserializer=wonderland__pb2.ListJobsRequest.FromString,
          response_serializer=wonderland__pb2.ListOfJobs.SerializeToString,
      ),
      'ModifyJob': grpc.unary_unary_rpc_method_handler(
          servicer.ModifyJob,
          request_deserializer=wonderland__pb2.Job.FromString,
          response_serializer=wonderland__pb2.Job.SerializeToString,
      ),
      'PullPendingJobs': grpc.unary_unary_rpc_method_handler(
          servicer.PullPendingJobs,
          request_deserializer=wonderland__pb2.ListJobsRequest.FromString,
          response_serializer=wonderland__pb2.ListOfJobs.SerializeToString,
      ),
      'DeleteJob': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteJob,
          request_deserializer=wonderland__pb2.RequestWithId.FromString,
          response_serializer=wonderland__pb2.Job.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Wonderland', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
