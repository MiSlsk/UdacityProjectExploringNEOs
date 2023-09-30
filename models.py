"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""


from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **kwargs):
        """Create a new `NearEarthObject`.

        :param kwargs: A dictionary of excess keyword arguments supplied to the constructor.

        Commonly used parameters:
        :param str designation: The NEO’s primary designation.
        :param str name: The NEO’s IAU name (could be empty, or None).
        :param float diameter: The NEO’s diameter, in kilometers, or NaN.
        :param bool hazardous: Whether the NEO is potentially hazardous.
        :param list approaches: A collection of this NEO’s CloseApproaches (initially an empty collection).
        """
        self.designation = (kwargs.get('designation') if kwargs.get('designation') else '')
        self.name = (kwargs.get('name') if kwargs.get('name') else None)
        self.diameter = (float(kwargs.get('diameter')) if kwargs.get('diameter') else float('nan'))
        self.hazardous = (kwargs.get('hazardous') == 'Y')
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f"{self.designation} ({self.name})" if self.name else f"{self.designation}"

    @property
    def serialize(self):
        """Produce a dictionary containing relevant attributes for CSV or JSON serialization."""
        return {'designation': str(self.designation),
                'name': str(self.name) if self.name else '',
                'diameter_km': self.diameter,
                'potentially_hazardous': self.hazardous}

    def __str__(self):
        """Return `str(self)`."""
        verb = "is" if self.hazardous else "is not"
        return (f"NEO {self.fullname} "
                f"has a diameter of {self.diameter:.3f} km and "
                f"{verb} potentially hazardous.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **kwargs):
        """Create a new `CloseApproach`.

        :param kwargs: A dictionary of excess keyword arguments supplied to the constructor.

        Commonly used parameters:
        :param str designation: An additional attribute, to store the NEO’s primary designation
                                before the CloseApproach is linked to its NearEarthObject.
        :param str time: The date and time, in UTC, at which the NEO passes closest to Earth.
        :param float distance: The nominal approach distance, in astronomical units,
                               of the NEO to Earth at the closest point.
        :param float velocity: The velocity, in kilometers per second,
                               of the NEO relative to Earth at the closest point.
        :param NearEarthObject neo: A reference to the NearEarthObject that is making the close approach
                                    (initially None).
        """
        self._designation = (kwargs.get('designation') if kwargs.get('designation') else '')
        self.time = (cd_to_datetime(kwargs.get('time')) if kwargs.get('time') else None)
        self.distance = (float(kwargs.get('distance')) if kwargs.get('distance') else 0.0)
        self.velocity = (float(kwargs.get('velocity')) if kwargs.get('velocity') else 0.0)
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time) if self.time is not None else 'n/a date'

    @property
    def fullname(self):
        """Return a representation of the full name of for this object."""
        return f"{self.neo.fullname}" if self.neo else f"{self._designation}"

    @property
    def serialize(self):
        """Produce a dictionary containing relevant attributes for CSV or JSON serialization."""
        return {'datetime_utc': datetime_to_str(self.time) if self.time else '',
                'distance_au': self.distance,
                'velocity_km_s': self.velocity,
                'neo': self.neo.serialize}

    def __str__(self):
        """Return `str(self)`."""
        return (f"On {self.time_str}, '{self.fullname}' "
                f"approaches Earth at a distance of {self.distance:.2f} au and "
                f"a velocity of {self.velocity:.2f} km/s.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")
