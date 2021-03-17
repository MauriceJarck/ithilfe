class Device:
    """Device parent class
    base of all more specified device classes"""
    def __init__(self, name: str, user: str, comment: str, datetime: str) -> None:
        """inits Device class
        configuring parameters of Device class
        Args:
            name: defines devicename of registered device
            user: defines username of registered device
            comment: defines comment of registered device to point out some thing worth knowing
            datetime: defines date and time when registration was made
        Returns:
            None
        """

        self.name = name
        self.user = user
        self.OS = None
        self.comment = comment
        self.datetime = datetime

    def __str__(self) -> str:
        """overwrites str method
        houses readable information of Device parameters
        Returns:
            String representation of Device instance
        """
        return f"{self.name}, {self.user}, {self.OS}, {self.__class__.__name__}, {self.comment}, {self.datetime}"

    visible_attr = ["user", "OS"]
    """list of attributes which can be modified by the user"""



class WindowsLapTop(Device):
    """
    specifies Device class and adds exta status variables
    """
    def __init__(self, name: str, user: str, comment: str, datetime: str) -> None:
        """inits Device class
            configuring parameters of Device class
            Args:
                name: defines devicename of registered device
                user: defines username of registered device
                comment: defines comment of registered device to point out some thing worth knowing
                datetime: defines date and time when registration was made
            Returns:
                None
            """
        super().__init__(name, user, comment, datetime)
        self.bitlockkey = 1234
        """int: example of attribute not beeing visible to user"""
        self.largerBattery = True
        """bool: example of extra attribute describing class"""
        self.upgradedCPU = False
        """bool: example of extra attribute describing class"""

    def __str__(self):
        """overwrites str method
            houses readable information of Device parameters
            Returns:
                String representation of Device instance
            """
        return f"{self.name}, {self.user}, {self.OS}, {self.__class__.__name__}, largerbattery: {self.largerBattery}, upgradedCPU: {self.upgradedCPU}"

    expected_OS = ["Win10", "Win7"]
    """list: possible os which to this device type"""

    visible_attr = ["user", "OS", "largerBattery", "upgradedCPU"]
    """list: attributes which can be modified by the user overwrites same attribute of Device class"""



class WindowsWorkStation(Device):
    """specifies Device class and adds exta status variables
        """
    expected_OS = ["Win10", "Win7"]
    """list: possible os which to this device type"""


class Macbook(Device):
    """specifies Device class and adds exta status variables
            """
    expected_OS = ["MacOS"]
    """list: possible os which to this device type"""