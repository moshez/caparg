"""
Implementation of argument parsing.

Should not be imported directly by user code.
"""

import argparse

import attr
import pyrsistent


@attr.s(frozen=True)
class _Command(object):

    """
    Top-level command or subcommand
    """

    _name = attr.ib()
    _args = attr.ib()
    _options = attr.ib()


    def rename(self, new_name):
        """
        Return a new command with a different name
        """
        return attr.evolve(self, name=pyrsistent.pvector(new_name.split()))

    def _make_parser(self):
        my_options = self._options
        subcommands = pyrsistent.m()
        for thing in self._args:
            my_options += thing.get_options()
        for thing in self._args:
            for name, subcommand in thing.add_to(self._name, my_options):
                subcommands = subcommands.set(name, subcommand)
        return _Parser(subcommands)

    def get_options(self):
        """
        Options that should only be inherited

        Returns:
            empty immutable iterable
        """
        return pyrsistent.v()

    def add_to(self, parent_name, my_options):
        """
        Command-line details to add to subparser

        Args:
            parent_name (List[str]): name of parent
            my_options (Dict[str,thing]): inherited options

        Returns:
           a tuple: (full_name, options)
        """
        full_name = parent_name + self._name
        for thing in self._args:
            my_options += thing.get_options()
        for thing in self._args:
            for name, suboptions in thing.add_to(full_name, my_options):
                yield name, suboptions
        if self._name:
            yield full_name, my_options + self._options

    def parse(self, args):
        """
        Parse command-line

        Args:
            args (List[str]): command-line arguments

        Returns:
            immutable map with __caparg_subcommand__ as one of the keys
        """
        parser = self._make_parser()
        return parser.parse_args(args)


@attr.s(frozen=True)
class ParseError(ValueError):

    """
    Command-line arguments are invalid
    """

    message = attr.ib()


class _RaisingArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        raise ParseError(message)


@attr.s(frozen=True)
class _Parser(object):

    _subcommands = attr.ib()

    def parse_args(self, args):
        """
        Parse arguments

        Args:
            args (List[str]): command-line arguments

        Returns:
            immutable map, where one of the keys is __caparg_subcommand__
        """
        args = pyrsistent.pvector(args)
        candidates = [i
                      for i in range(1, len(args)+1)
                      if args[:i] in self._subcommands]
        if not candidates:
            raise ParseError(self._make_help())
        parts = max(candidates)
        subcommand, rest = self._subcommands[args[:parts]], args[parts:]
        parser = _RaisingArgumentParser(' '.join(args[:parts]))
        for thing in subcommand:
            thing.add_argument(parser)
        namespace = parser.parse_args(rest)
        ret = pyrsistent.m(__caparg_subcommand__=args[:parts])
        for thing in subcommand:
            ret = ret.update(thing.get_value(namespace))
        return ret

    def _make_help(self):
        parts = ["Usage:\n"]
        for key in sorted(self._subcommands):
            parts.append("    " + " ".join(key) + "\n")
        return ''.join(parts)


@attr.s(frozen=True)
class _PreOption(object):

    """
    Something that could be turned into an option

    An option that lacks a name.
    """

    _type = attr.ib()
    _required = attr.ib(default=False)
    _have_default = attr.ib(default=False)

    @attr.s(frozen=True)
    class Option(object):

        """
        An option
        """

        _type = attr.ib()
        _required = attr.ib()
        _have_default = attr.ib()
        _name = attr.ib()
        _MISSING = object()

        def add_argument(self, parser):
            """
            Add ourselves to an argument parser

            Args:
                parser (argparse.ArgumentParser): the parser to add to
            """
            if self._type == str:
                parser.add_argument('--' + self._name,
                                    type=str,
                                    required=self._required,
                                    default=self._MISSING)
                return
            if self._type == bool:
                parser.add_argument('--' + self._name, action='store_true',
                                    default=False)
                return
            raise NotImplementedError("cannot add to parser",
                                      self, parser)  # pragma: no cover

        def get_value(self, namespace):
            """
            Get value out of a namespace

            Args:
                namespace (argparse.Namespace): the namespace

            Returns:
                a value
            """
            value = getattr(namespace, self._name, self._MISSING)
            ret = pyrsistent.m()
            if value is not self._MISSING:
                ret = ret.set(self._name, value)
            elif self._have_default is True:
                if self._type == str:
                    ret = ret.set(self._name, '')
                else:  # pragma: no cover
                    raise NotImplementedError("cannot default value",
                                              self._name, self._type)
            return ret

    def with_name(self, name):
        """
        Save a name

        Args:
            name (str): The name of the option

        Returns:
            something with add_argument and get_value
        """
        return self.Option(name=name, type=self._type, required=self._required,
                           have_default=self._have_default)


def command(_name, *args, **kwargs):
    """
    A command (or a subcommand)

    Args:
        _name (str): the name of the subcommand (for top-level, '')
        *args (tuple): commands and options
        **kwargs (dict): options by name
    """
    _name = pyrsistent.pvector(_name.split())
    my_options = pyrsistent.pvector(value.with_name(key)
                                    for key, value in kwargs.items())
    return _Command(_name, args, my_options)


# pylint: disable=redefined-builtin
def option(type, required=False, have_default=False):
    """
    An option

    Note that an option does not know its name. It will usually be used
    in a dictionary where the name is specified as its key, and it has
    a method :code:`with_name` to add the name when processed.

    Args:
        type (class): the expected input type
        required (bool): whether option name is expected
        have_default (bool): whether to auto-create a default based on the type
    """
    return _PreOption(type, required=required, have_default=have_default)
# pylint: enable=redefined-builtin


@attr.s(frozen=True)
class _OptionList(object):

    """List of options"""

    _options = attr.ib(convert=lambda x:
                       pyrsistent.pvector(value.with_name(key)
                                          for key, value in x.items()))

    def get_options(self):
        """
        Return options for current command and subcommands.

        Returns:
            immutable iterable of things with add_argument and get_value
        """
        return self._options

    def add_to(self, _parent_name, _options):
        """
        Return subcommands to be added

        Args:
            parent_name (List[str]): full name of the parent
            options (List[option interface?]): list of options to inherit

        Returns:
            empty immutable iterable
        """
        return pyrsistent.v()


def options(**kwargs):
    """
    Wrap options

    This is used to be able to put options at the beginning of the
    argument list of a command. Since options are given by keywords,
    they must follow positional arguments."

    Args:
        **kwargs (Dict[str, option]): Mapping
    """
    return _OptionList(pyrsistent.pmap(kwargs))


@attr.s(frozen=True)
class _Positional(object):

    """
    Positional argument
    """

    _name = attr.ib()
    _type = attr.ib()
    _required = attr.ib()
    _have_default = attr.ib()
    _MISSING = object()

    def get_options(self):
        """
        Return options to be added to current and sub-parsers

        Returns:
            immutable iterable containing self
        """
        return pyrsistent.v(self)

    def add_to(self, _parent_name, _options):
        """
        Return subcommands to be added

        Args:
            parent_name (List[str]): full name of the parent
            options (List[option interface?]): list of options to inherit

        Returns:
            empty immutable iterable
        """
        return pyrsistent.v()

    def add_argument(self, parser):
        """
        Add ourselves to a :code:`argparse.ArgumentParser`

        Add details of class to an :code:`ArgumentParser` which
        will parse this positional.

        Args:
            parser (argparse.ArgumentParser): the parser
        """
        if self._have_default:
            raise NotImplementedError("cannot have defaults in positionals",
                                      self._name)  # pragma: no cover
        if self._type == str:
            parser.add_argument(self._name, type=str, default=self._MISSING)
            return
        raise NotImplementedError("cannot add to parser",
                                  self, parser)  # pragma: no cover

    def get_value(self, namespace):
        """
        Get the value from a 'namespace'.

        Args:
            namespace (object): something with potentially the named attribute

        Returns:
            an immutable mapping which is either empty, or has one element
        """
        value = getattr(namespace, self._name, self._MISSING)
        ret = pyrsistent.m()
        if value is not self._MISSING:
            ret = ret.set(self._name, value)
        # argparse doesn't allow positionals to have defaults
        # elif self._have_default is True:
        #     if self._type == str:
        #         ret = ret.set(self._name, '')
        #     else:
        #         raise NotImplementedError("cannot default value",
        #                                   self._name, self._type)
        return ret


# pylint: disable=redefined-builtin
def positional(name, type, required=False, have_default=False):
    """
    A positional argument

    Args:
        name (str): name of argument
        type (type): expected type
        required (boolean): argument is required (default :code:`False`)
        have_default (boolean): if argument is not given, generate
                                a default (default :code:`False`)

    Returns:
        Something with add_to and get_value
    """
    return _Positional(name, type, required, have_default)
# pylint: enable=redefined-builtin
