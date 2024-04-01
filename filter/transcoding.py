from eventsourcing.persistence import Transcoding

from filter.data_models import Condition

class ConditionTranscoding(Transcoding):
    type = Condition
    name = 'condition'

    def encode(self, obj: Condition):
        return obj.model_dump()
    
    def decode(self, data):
        return Condition(**data)