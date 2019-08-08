import os
import json
import re
import sys

reload(sys)
sys.setdefaultencoding("utf8")


class IniData(object):
    def __init__(self):
        self._sections = dict()

    def has_section(self, section_name):
        """
        check if the given data/name has section
        :param section_name: section name of the ini data
        :return: status if the data has section
        """
        return self._sections.has_key(section_name)

    def add_section(self, section_name):
        """
        add section/header to the ini data
        :param section_name:name of the section
        """
        if not self.has_section(section_name):
            self._sections[section_name] = dict()

    def set(self, section_name, param_name, param_value):
        """
        set the section name, param name and value to the ini data
        :param section_name: name of section
        :param param_name: name of param
        :param param_value: value of the param
        """
        if not self.has_section(section_name):
            self.add_section(section_name)
        self._sections[section_name][param_name] = param_value

    def write(self, file_obj):
        """
        write the section and its param name and value to the
        ini file
        :param file_obj: obj contains param name and value
        """
        for section_name in sorted(self._sections):
            file_obj.write('[{}]\n'.format(section_name))
            try:
                section_params = self._sections.get(section_name)
                for param_name, param_value in section_params.items():
                    if type(param_value) is unicode:
                        if re.search("[\\r\\n\\t]", param_value):
                            param_value = str(param_value).encode('string_escape').replace('\"', '\\"')
                        param_value = "\"{}\"".format(param_value)
                        file_obj.write('{} = {}\n'.format(param_name, param_value))
                    else:
                        file_obj.write('{} = {}\n'.format(param_name, param_value))

            except Exception as e:
                print(e)
            file_obj.write('\n')


class ConvertJson2INI(object):
    """
    This class provies set of methods to read json file for sections and key value pairs.
    and to convert the json file to the .ini file.
    """

    def __init__(self, base, path, split_json=False):
        self.path = path
        self.base_key = base
        self.json_data = None
        self.ini_data = None
        self.split_json = split_json
        self.inputs = []

    def check_base(self):
        """
        base key to be appended for the ini file header
        :return:
        """
        if self.base_key is None:
            print('BASE_KEY is empty we can\'t proceed.')
            return False
        return True

    def read_json(self, src_path):
        """
        read the json file from the given path.
        :param src_path: path to the json file
        """
        if self.check_base():
            if not os.path.exists(src_path) and not os.path.isfile(src_path):
                print('{} is not exists/not a file.'.format(src_path))
                return
            with open(src_path) as json_data_file:
                print('loaded json')
                self.json_data = json.load(json_data_file)

    def convert(self):
        """
        start converting the json file (key and its data)
        and add it to the ini_data.
        :return:
        """
        if self.check_base():
            if self.json_data is None:
                print('Please read the JSON file, to convert.')
                return
            self.ini_data = IniData()
            self.add_dict_params(self.base_key, self.json_data)

    def add_dict_params(self, base_key, param_obj):
        """
        Some keys need to removed from the ini data .
        add key value pair as param obj to the ini data.
        :param base_key: key data or header
        :param param_obj: section name and its value
        """
        for dict_key, dict_value in param_obj.iteritems():
            if dict_key.strip() == 'xxx.ini':
                self.write_data(self.path,'App'+dict_key.strip(),dict_value)
            elif dict_key != 'SubService' and base_key!='Service':
                self.add_param(base_key, dict_key, dict_value)

    def add_param(self, base_key, param_name, param_value):
        """
        add name and value as params in the ini_data.
        :param base_key: header of the section
        :param param_name: key or  name
        :param param_value: value of the key
        """
        if self.split_json:
            if not base_key == '':
                json_path = self.path+os.sep+base_key
                filename = param_name
                self.write_data(json_path,filename, param_value)
        if isinstance(param_value, dict) or isinstance(param_value, list):
            if not base_key == '':
                new_key = base_key + '.' + param_name
            else:
                new_key = param_name
            if isinstance(param_value, dict):
                self.add_dict_params(new_key, param_value)
            elif isinstance(param_value, list):
                print('Params List: {} - {}'.format(new_key, param_value))
        else:
            if not self.ini_data.has_section(base_key):
                self.ini_data.add_section(base_key)
            self.ini_data.set(base_key, param_name, param_value)

    def write_ini(self, tar_path):
        """
        Once all the key value pair of json data is added to the ini data.
        write the ini data in file (ini)
        :param tar_path:
        :return:
        """
        if self.check_base():
            if self.ini_data is None:
                print('Please convert the JSON file, to write.')
                return
            if os.path.exists(tar_path):
                print('{} is exists, please give another file.'.format(tar_path))
                return
            ini_file = open(tar_path, mode='w')
            self.ini_data.write(ini_file)
            ini_file.close()

    def write_data(self, path, filename, ini_data):
        """
        write key value pair in file as raw data.
        :param path: path of the destination file
        :param filename: name of the destination file
        :param ini_data: data to be written in the file
        """
        try:
            if not os.path.exists(path):
                os.makedirs(path, 0755)
            filename = os.path.join(os.path.abspath(path), filename)
            with open(filename, 'w') as outfile:
                outfile.write(ini_data)
        except Exception as e:
            print(e)

    def get_inputs(self):
        """
        get the inputs name while parsing json file.
        :return: return a list of inputs
        """
        inputs = set(self.inputs)
        if inputs.__contains__('system'):
            inputs.remove('system')
        return list(inputs)

    def convert_to_ini(self, json_file_path, ini_file_path):
        """
        once the json contents are parsed , convert json data to the ini file.
        :param json_file_path: json file path
        :param ini_file_path: ini file path
        :return: status of converted boolean
        """
        converted = True
        try:
            self.read_json(json_file_path)
            self.convert()
            self.write_ini(ini_file_path)
        except Exception as e:
            converted = False
            print("Error in Converting Json to ini File {0}".format(e))
        return converted

    def split_json(self, json_file_path):
        """
        Dedicated method .
        split json file of kpi equations data and split it
        according and save it in the inputs specific folders.
        :param json_file_path: json file path
        :return: status of the splited_up boolean
        """
        splitted_up = True
        try:
            self.read_json(json_file_path)
            self.convert()
        except Exception as e:
            splitted_up = False
            print("Error in Converting Json to ini File {0}".format(e))
        return splitted_up