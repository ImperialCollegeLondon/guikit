"""
Contains the definition of the top window of the program, including the menu bar, the
toolbar (if any), the central widget, bottom progress bar and status area.
In particular, the progress bar and the status area are the kind of things that the
plugins will be importing - or at least wanting to update - regularly. They are defined
as singletons such that even though an instance is created once, such an instance can
be access directly from the class anywhere else where you import the class.
"""
