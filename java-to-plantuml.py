import argparse
from enum import Enum
import re

class Visibility(Enum):
    VOID = ""
    PUBLIC = "+"
    PROTECTED = "#"
    PRIVATE = "-"

    @classmethod
    def to_string(cls, vis) -> str:
        if (vis is None):
            return Visibility.VOID
        
        return vis

    @classmethod
    def from_string(cls, vis: str = None):
        if (vis is None):
            return Visibility.VOID
        
        vis = vis.strip().lower()

        if ("private" == vis):
            return Visibility.PRIVATE

        if ("protected" == vis):
            return Visibility.PROTECTED

        if ("public" == vis):
            return Visibility.PUBLIC
        
        return Visibility.VOID

class Attribute:
    def __init__(self, name: str, attr_type: str, visibility: Visibility = None) -> None:
        self.name = name
        self.attr_type = attr_type
        self.visibility = visibility

    def __str__(self) -> str:
        return "{}member(\"{}\", {})".format(self.visibility.value, self.attr_type, self.name)

class Method:
    def __init__(self, name: str, 
                return_type: str = None, 
                visibility: Visibility = None, 
                arguments_types: list[str] = None) -> None:
        self.name = name
        self.return_type = return_type
        self.visibility = visibility
        self.arguments_types = [] if not arguments_types else arguments_types

    def __str__(self) -> str:
        return "{}member(\"{}\", \"{}({})\")".format(
            self.visibility.value, 
            self.return_type,
            self.name,
            ",".join(self.arguments_types))

class JavaClass:
    def __init__(self, name: str, attributes: list[Attribute] = None, methods: list[Method] = None) -> None:
        self.name = name
        self.attributes = [] if not attributes else attributes
        self.methods = [] if not methods else methods

    def __str__(self) -> str:
        attributes_string = "\n".join(["  " + str(_) for _ in self.attributes])
        methods_string = "\n".join(["  " + str(_) for _ in self.methods])

        response = "class " + self.name + " {\n"
        response+= "{}\n".format(attributes_string)
        response+= "{}\n".format(methods_string)
        response+= "} \n"

        return response

class Package:
    def __init__(self, name: str, classes: list[JavaClass] = None, packages: list = None) -> None:
        self.name = name
        self.classes = [] if not classes else classes
        self.packages = [] if not packages else packages

    def __str__(self) -> str:
        classes_string = "\n".join([_.__str__() for _ in self.classes])
        packages_string = "\n".join([_.__str__() for _ in self.packages])

        response = "package " + self.name + " {\n"
        response += "{}\n".format(classes_string)
        response += "{}\n".format(packages_string)
        response += "}\n"

        return response

# re_methods = r"\s*(public|private|protected)?\s*(static)?\s*(?:@[a-zA-Z_][a-zA-Z0-9_]*(?:\([^)]*\))?\s+)*(?![a-zA-Z_])\s*([a-zA-Z_][a-zA-Z0-9_]*\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)\s*({)?\s*\n"
re_methods = r"\s*(public|private|protected)?\s*(static)?\s*(?:@[a-zA-Z_][a-zA-Z0-9_]*(?:\([^)]*\))?\s+)*(?![a-zA-Z_])\s*(\w+(\[\])?(\s*<\s*\w+\s*>)?\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)\s*({)?\s*\n"

re_attributes = r"^\s*(public|private|protected)?\s+(?!class|return|package)(\w+(\[\])?(\s*<\s*\w+\s*>)?)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*;"

re_parameters = r'\b\w+(?:<\w+>)?\b(?=\s+\w+|$)'

def get_attributes(content: str) -> list[Attribute]:
    attributes = []

    matches = re.finditer(re_attributes, content, re.MULTILINE)

    # Iterate over the matches
    for match in matches:
        visibility = match.group(1)
        attribute_type = match.group(2)
        attribute_name = match.group(5)

        attributes.append(Attribute(attribute_name, attribute_type, Visibility.from_string(visibility)))

    return attributes

def get_methods(content: str) -> list[Attribute]:
    def __get_arguments_types(arguments: str) -> list[str]:
        return re.findall(re_parameters, arguments)
    
    methods = []

    matches = re.finditer(re_methods, content, re.MULTILINE)

    # Iterate over the matches
    for match in matches:
        visibility = match.group(1)
        is_static = match.group(2)
        return_type = match.group(3)
        method_name = match.group(6)
        parameters = match.group(7)

        methods.append(Method(method_name,
            return_type,
            Visibility.from_string(visibility),
            __get_arguments_types(parameters)))

    return methods


class PlantUmlAdapter:
    def __init__(self, content: str) -> None:
        self.content = content
        # TODO Faire en sorte que pour chaque contenu, on puisse extraire la classe => penser au package

    

def test_regex():
    lines = []
    with open("test.java", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    content = "\n".join(lines)

    methods = (get_methods(content))

    for _ in methods:
        print(_.__str__())

def main():
    
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--path")
    parser.add_argument("--output")

    args = parser.parse_args()
    print(args.path)
    print(args.output)
    test_regex()

def test():
    a1 = Attribute("attribut1", "int", Visibility.PRIVATE)
    a2 = Attribute("attribut2", "int", Visibility.VOID)
    m1 = Method("nom", "void", Visibility.PRIVATE, ['String', 'Integer', 'List<Integer>'])

    c1 = JavaClass("MaClasse", [a1, a2], [m1])

    p1 = Package("fr.bpce.frf", [c1, JavaClass("ClasseVide")], [Package("package.vide")])

    print(a1, a2, m1, c1, JavaClass("ClasseVide"), p1, sep="\n")

if __name__ == '__main__':
    main()
