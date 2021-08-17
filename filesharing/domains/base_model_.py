import pprint
import typing

import six

T = typing.TypeVar("T")


class Model(object):
    # openapiTypes: The key is attribute name and the
    # value is attribute type.
    openapi_types = {}

    # attributeMap: The key is attribute name and the
    # value is json key in definition.
    attribute_map = {}

    @classmethod
    def from_dict(cls: typing.Type[T], dikt) -> T:
        """Returns the dict as a model"""
        return util.deserialize_model(dikt, cls)

    def to_dict(self, map_keys=False):
        """Returns the model properties as a dict

        :rtype: dict
        """
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            self.add_attr_to_dict(result, map_keys, attr, _)

        if map_keys:
            # replace keys using attribute map in reverse for each response if different
            for item in self.attribute_map.items():
                if item[1] != item[0]:
                    result[item[1]] = result[item[0]]
                    del result[item[0]]

        return result

    def add_attr_to_dict(self, result: dict, map_keys: bool, attr, _):
        value = getattr(self, attr)
        if isinstance(value, list):
            result[attr] = list(
                map(
                    lambda x: x.to_dict(map_keys) if hasattr(x, "to_dict") else x, value
                )
            )
        elif hasattr(value, "to_dict"):
            result[attr] = value.to_dict(map_keys)
        elif isinstance(value, dict):
            result[attr] = dict(
                map(
                    lambda item: (item[0], item[1].to_dict(map_keys))
                    if hasattr(item[1], "to_dict")
                    else item,
                    value.items(),
                )
            )
        else:
            result[attr] = value

    def to_str(self):
        """Returns the string representation of the model

        :rtype: str
        """
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
