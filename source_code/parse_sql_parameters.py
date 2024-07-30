
class ParseSqlParameters:

    """
    --- parameters start
    DECLARE @Parameter1 INT = <value>; --- Prompt for input1 ?
    DECLARE @Parameter2 INT = <value>; --- Prompt for input2 ?
    DECLARE @Parameter3 INT = <value>; --- Prompt for input3 ?
    DECLARE @Parameter4 INT = <value>;
    --- parameters end
    --- with results

    Other text
    """

    @staticmethod
    def find_parameter_section_start_end(file_data: str) -> dict[str, int]:
        parameter_start_index = file_data.find('--- parameters start')
        parameter_end_index = file_data.find('--- parameters end')
        return {'start_index': parameter_start_index, 'end_index': parameter_end_index}

    def has_parameter_section(self, file_data: str) -> bool:
        indexes = self.find_parameter_section_start_end(file_data)
        if indexes['start_index'] > -1 and indexes['end_index'] > -1:
            return True
        return False

    def extract_parameters_section(self, file_data: str) -> list[str]:
        start_section = '--- parameters start'
        indexes = self.find_parameter_section_start_end(file_data)
        parameter_section = file_data[indexes['start_index']: indexes['end_index']]
        parameter_section = parameter_section.replace(start_section, '')
        parameters = parameter_section.split('\n')
        return parameters

    @staticmethod
    def extract_parameters(parameter_line: str) -> dict[str, str]:
        end_of_sql_line_index = parameter_line.find(';') + 1
        sql_line = parameter_line[: end_of_sql_line_index]
        prompt = parameter_line[end_of_sql_line_index:].strip()
        parameters = sql_line.split(' ')
        return {'original_line': parameter_line, 'parameter_type': parameters[2],
                'parameter': parameters[1], 'prompt': prompt}

    @staticmethod
    def prompt_user(prompt_data: list[dict[str, str]]) -> None:
        for prompt in prompt_data:
            prompt_value = prompt['prompt']
            if not prompt_value:
                prompt_value = f"Enter value for {prompt['parameter']} ?"
            prompt_value = prompt_value.replace('-', '')
            response = input(prompt_value + ' ')
            if not response.isnumeric():
                if not response == 'NULL':
                    response = f"'{response}'"
            prompt['response'] = prompt['original_line'].replace('<value>', response)

    @staticmethod
    def replace_parameter_values(prompt_data: list[dict[str, str]], sql_script: str) -> str:
        for prompt in prompt_data:
            sql_script = sql_script.replace(prompt['original_line'], prompt['response'])
        return sql_script

    def replace_parameters_with_prompts(self, sql_script_input: str) -> dict[str, str]:
        adjusted_sql = sql_script_input
        has_parameters = self.has_parameter_section(sql_script_input)
        if has_parameters:
            p_sections = self.extract_parameters_section(sql_script_input)
            prompt_data = []
            for p_section in p_sections:
                if p_section != '':
                    processed_parameters = self.extract_parameters(p_section)
                    prompt_data.append(processed_parameters)
            self.prompt_user(prompt_data)
            adjusted_sql = self.replace_parameter_values(prompt_data, sql_script_input)
        with_return_results = self.check_for_return_results_marker(sql_script_input)
        return {'sql_script': adjusted_sql, 'return_results': with_return_results}

    @staticmethod
    def check_for_return_results_marker(sql_script_input: str) -> bool:
        index_with_result = sql_script_input.find('--- with results')
        if index_with_result > -1:
            return True
        return False

    @staticmethod
    def read_file(path_file: str) -> str:
        text_file = open(path_file, "r")
        file_data = text_file.read()
        text_file.close()
        return file_data
