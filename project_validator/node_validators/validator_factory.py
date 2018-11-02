import xml.etree.ElementTree as ElementTree

from ..node_validators.annotation_validator import AnnotationValidator
from ..node_validators.body_validator import BodyValidator


class ValidatorFactory:

    _validators = {}
    _validator_mapper = {
        'annotation-contains': AnnotationValidator,
        'body-contains': BodyValidator,
    }

    @staticmethod
    def load_validators(path: str):
        validators_conf = ElementTree.parse(path).getroot()
        ValidatorFactory._validators.clear()

        for validator in validators_conf:

            try:
                attr = validator.attrib['attribute']
                ValidatorFactory._validators[attr] = ValidatorFactory._validator_mapper[attr](validator)
            except KeyError:
                raise ResourceWarning('used a node_validators that its class does not exist! (validators.xml)')

    @staticmethod
    def get_validator_by_attr(name: str) -> AnnotationValidator:
        if len(ValidatorFactory._validators) == 0:
            raise LookupError('validation factory didn\'t initialized well')
        return ValidatorFactory._validators[name]

    @staticmethod
    def has_validator(attr: str) -> bool:
        return attr in ValidatorFactory._validators
