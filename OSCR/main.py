from datetime import timedelta, datetime
import pickle
import time

from datamodels import Combat, LogLine
from iofunc import MAP_IDENTIFIERS_EXISTENCE
from iofunc import get_combat_log_data
from baseparser import analyze_shallow



class OSCR():

    version = '2024.01b310'

    def __init__(self, log_path:str = None, settings:dict = None):
        self.log_path = log_path
        self.combats = list()
        self.excess_log_lines = list()
        self._settings = {
            'combats_to_parse': 10,
            'seconds_between_combats': 100,
            'excluding_event_ids': ['Autodesc.Combatevent.Falling'],
            'graph_resolution': 0.2
        }
        if settings is not None:
            self.merge_settings(settings)

    def merge_settings(self, new_settings:dict):
        for key, value in new_settings.items():
            if key in self._settings:
                self._settings[key] = value

    def identfy_map(self, entity_id:str) -> str | None:
        '''
        Identify map by checking whether the entity supplied identifies a map. Returns map name or None.
        '''
        try:
            clean_entity_id = entity_id.split(' ', maxsplit=1)[1].split(']', maxsplit=1)[0]
        except IndexError:
            return None
        if clean_entity_id in MAP_IDENTIFIERS_EXISTENCE:
            return MAP_IDENTIFIERS_EXISTENCE[clean_entity_id]
        return None
        
    def to_datetime(self, date_time:str):
        '''
        returns datetime object from combatlog string containing date and time
        '''
        date_time_list = date_time.split(':')
        date_time_list += date_time_list.pop().split('.')
        date_time_list = list(map(int, date_time_list))
        date_time_list[0] += 2000
        date_time_list[6] *= 100000
        return datetime(*date_time_list)
        

    def analyze_log_file(self, total_combats:int | None = None, extend:bool = False):
        '''
        Analyzes the combat at self.log_path and replaces self.combats with the newly parsed combats.
        
        Parameters:
        - :param total_combats: holds the number of combats that should be in self.combats after the method is 
        finished.
        - :param extend: extends the list of current combats to match the number of total_combats by analyzing
        excess_log_lines
        '''
        if self.log_path is None:
            raise AttributeError('self.log_path must contain a path to a log file.')
        if total_combats is None:
            total_combats = self._settings['combats_to_parse']
        if extend:
            if total_combats <= len(self.combats):
                return
            log_lines = self.excess_log_lines
        else:
            log_lines = get_combat_log_data(self.log_path)
            log_lines.reverse()
            self.combats = list()
            self.excess_log_lines = list()
        combat_delta = timedelta(seconds=self._settings['seconds_between_combats'])
        current_combat_lines = list()
        current_combat = None
        map_identified = False
        last_log_time = self.to_datetime(log_lines[0].split('::')[0]) + 2 * combat_delta

        for line_num, line in enumerate(log_lines):
            time_data, attack_data = line.split('::')
            log_time = self.to_datetime(time_data)
            if last_log_time - log_time > combat_delta:
                if current_combat is not None:
                    if not (len(current_combat_lines) < 20 
                            and current_combat_lines[0].event_id in self._settings['excluding_event_ids']):
                        current_combat_lines.reverse()
                        current_combat.log_data = current_combat_lines
                        current_combat.date_time = last_log_time
                        self.combats.append(current_combat)
                    if len(self.combats) == self._settings['combats_to_parse']:
                        self.excess_log_lines = log_lines[line_num:]
                        break
                current_combat_lines = list()
                current_combat = Combat()
                map_identified = False
            splitted_line = attack_data.split(',')
            current_line = LogLine(log_time, 
                    *splitted_line[:10],
                    float(splitted_line[10]),
                    float(splitted_line[11])
                    )
            if not map_identified:
                current_map = self.identfy_map(current_line.target_id)
                if current_map is not None:
                    current_combat.map = current_map
                    map_identified = True
   
            last_log_time = log_time
            current_combat_lines.append(current_line)

    def shallow_combat_analysis(self, combat_num:int) -> tuple[list]:
        '''
        Analyzes combat from currently available combats in self.combat.

        Parameters:
        - :param combat_num: index of the combat in self.combats

        :return: tuple containing the overview table, DPS graph data and DMG graph data
        '''
        try:
            analyze_shallow(self.combats[combat_num], self._settings)
            return (self.combats[combat_num].table,
                    self.combats[combat_num].graph_data)
        except IndexError:
            raise AttributeError(f'Combat #{combat_num} you are trying to analyze has not been isolated yet.'
                                 f'Number of isolated combats: {len(self.combats)} -- '
                                 'Use OSCR.analyze_log_files() with appropriate arguments first.')

# if __name__ == '__main__':
#     test_parser = OSCR('combatlog.log')
#     t1 = time.time()
#     test_parser.analyze_log_file()
#     output = test_parser.shallow_combat_analysis(2)
#     t2 = time.time()
#     print(float(t2-t1))
#     print(output)
#     print('end')
    
                


            



    

    
