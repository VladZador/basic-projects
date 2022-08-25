import csv
from xml.etree import ElementTree as ET
import json


class CSV_File:
    def __init__(self):
        pass

    def _file_creator(self, filename):
        headers = ["Name", "Surname", "Birthday", "City"]
        with open(filename, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(headers)


    def _data_writer(self, filename):
        try:
            with open(filename, "r", newline="") as csv_file:
                csv_reader = csv.reader(csv_file)
                # Since mode "a" in open() method creates a file if it doesn't exist, this reading command is used for checking whether the file exist.
            with open(filename, "a", newline="") as csv_file:
                csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([input("Enter a name: "),
                                    input("Enter a surname: "),
                                    input("Enter a birthday: "),
                                    input("Enter a city: ")])
                print("\nThe data has been recorded to the " + filename + "\n")
        except FileNotFoundError:
            print("\nSorry, there is no file with such name\n")

    def _data_reader(self, filename):
        try:
            with open(filename, "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                data = [row for row in csv_reader]
                print("\n",data,"\n")
        except FileNotFoundError:
            print("\nSorry, there is no file with such name\n")


class Converter:
    def __init__(self):
        pass

    def _csv_split(self, filename):
        data = self.__data_reader(filename)
        keys = data[0]
        data.pop(0)
        return keys, data

    def __data_reader(self, filename):
        try:
            with open(filename, "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                data = [row for row in csv_reader]
                return data
        except FileNotFoundError:
            print("\nSorry, there is no file with such name\n")

    def _change_filename(self, filename, extension):
        filename_plus_extension = filename.split(".")
        filename = filename_plus_extension[0]+extension
        return filename


class JSON_Converter(Converter):
    def __init__(self):
        self._extension = ".json"

    def _convert_to_json(self, filename):
        keys, data = self._csv_split(filename)
        if keys and data:
            json_list_of_dicts = self.__list_creator(keys, data)
            filename_json = self._change_filename(filename, self._extension)
            with open(filename_json, "w") as json_file:
                json.dump(json_list_of_dicts, json_file)
            print("\n"+filename+" has been successfully converted to "+filename_json+"\n")
        else:
            print("\n"+"Something wrong with the table in "+filename+"\n")

    def __list_creator(self, keys, data):
        list_of_dicts = []
        for person in data:
            json_dict = self.__dict_creator(keys, person)
            list_of_dicts.append(json_dict)
        return list_of_dicts

    def __dict_creator(self, keys, some_list):
        json_dict = {}
        for i in range(len(some_list)):
            json_dict[keys[i]] = some_list[i]
        return json_dict


class XML_Converter(Converter):
    def __init__(self):
        self._extension = ".xml"

    def  _convert_to_xml(self, filename):
        keys, data = self._csv_split(filename)
        if keys and data:
            xml_data = self.__tree_creator(keys, data)
            filename_xml = self._change_filename(filename, self._extension)
            with open(filename_xml, "wb") as xml_file:
                xml_file.write(xml_data)
            print("\n"+filename+" has been successfully converted to "+filename_xml+"\n")
        else:
            print("\n"+"Something wrong with the table in "+filename+"\n")

    def __tree_creator(self, keys, data):
        xml_tree = ET.Element("root")
        person_holder = ET.SubElement(xml_tree, "people")
        id = 1
        for person in data:
            people = ET.SubElement(person_holder, "person")
            people.set("id", "{}".format(id))
            id += 1
            for i in range(len(keys)):
                elem = ET.SubElement(people, keys[i])
                elem.text = person[i]
        xml_data = ET.tostring(xml_tree)
        return xml_data


class XPATH:
    def __init__(self, filename):
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()

    def _find_person(self):
        number_of_elems = self.__counting_elements()
        id_number = input(f"""Currently there is information about {number_of_elems} people in the table
Enter person id: """)
        try:
            if 0 < int(id_number) <= number_of_elems:
                self.__actually_find_person(id_number)
            else:
                print("There is no such id number in the table")
                self._find_person()
        except ValueError:
            print("Enter a valid number")
            self._find_person()

    def __actually_find_person(self, id_number):
        name = self.root.findall(f"people/person[@id=\"{id_number}\"]/Name")
        surname = self.root.findall(f"people/person[@id=\"{id_number}\"]/Surname")
        birthday = self.root.findall(f"people/person[@id=\"{id_number}\"]/Birthday")
        city = self.root.findall(f"people/person[@id=\"{id_number}\"]/City")
        for values in zip(name, surname, birthday, city):
            row = {value.tag: value.text for value in values}
            print(row)

    def _find_value(self):
        number_of_elems = self.__counting_elements()
        id_number = input(f"""Currently there is information about {number_of_elems} people in the table
Enter person id: """)
        if 0 < int(id_number) <= number_of_elems:
            search_tag = input("Enter search tag (Name, surname, birthday or city): ").capitalize()
            value = self.root.find(f"people/person[@id=\"{id_number}\"]/{search_tag}").text
            if value:
                print(value)
            else:
                print("Wrong name or the element is empty")
                self._find_value()
        else:
            print("There is no such id number in the table")
            self._find_value()

    def __counting_elements(self):
        last_element = self.root.find("people/person[last()]")
        last_id = last_element.get("id")
        return int(last_id)


class Core:
    def __init__(self):
        pass

    def _option_processor(self, option):
        if option in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            self.__data_processor(option)
        else:
            try:
                opt_number = int(option)
                print("\nType a number between 1 and 8\n")
            except ValueError:
                print("\nType a number\n")

    def __data_processor(self, option):
        filename = input("Enter the name of the file as \"filename.csv\" or \"filename.xml\": ")
        if option in ["1", "2", "3", "4"]:
            self.__csv_processor(filename, option)
        elif option in ["5", "6"]:
            self.__convertor(filename, option)
        elif option in ["7", "8"]:
            self.__xml_processor(filename, option)

    def __csv_processor(self, filename, option):
        self._csv_file = CSV_File()
        if option == "1":
            self._csv_file._file_creator(filename)
            print("\nThe file " + filename + " has been created!\n")
        elif option == "2":
            self._csv_file._data_writer(filename)
        elif option == "3":
            self._csv_file._file_creator(filename)
            self._csv_file._data_writer(filename)
        elif option == "4":
            self._csv_file._data_reader(filename)

    def __convertor(self, filename, option):
        if option == "5":
            self._csv_file = XML_Converter()
            self._csv_file._convert_to_xml(filename)
        if option == "6":
            self._csv_file = JSON_Converter()
            self._csv_file._convert_to_json(filename)

    def __xml_processor(self, filename, option):
        self._xml_file = XPATH(filename)
        if option == "7":
            self._xml_file._find_person()
        if option == "8":
            self._xml_file._find_value()


class Application_Run:
    def __init__(self):
        self._core = Core()

    def run(self):
        while True:
            print("""Choose your option:
1. Create a new .csv file
2. Write data into the file
3. Rewrite the file
4. Read the file
5. Convert to XML
6. Convert to JSON
7. Search a person data in .xml file by id
8. Search a person tag value in .xml file""")
            option = input()
            self._core._option_processor(option)


if __name__ == "__main__":
    testfile = Application_Run()
    try:
        testfile.run()
    except KeyboardInterrupt:
        quit()
