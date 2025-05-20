import xml.etree.ElementTree as ET
from typing import List, Dict


class ConfigLoader:
    @staticmethod
    def load_config(filename: str) -> ET.ElementTree:
        try:
            return ET.parse(filename)
        except (FileNotFoundError, ET.ParseError) as e:
        
            raise

    @staticmethod
    def load_levels_config(filename: str) -> List[Dict]:
        try:
            tree = ConfigLoader.load_config(filename)
            root = tree.getroot()
            levels = []
            for level in root.findall('level'):
                level_data = {
                    'id': int(level.get('id')),
                    'target_score': int(level.find('target_score').text),
                    'time_limit': int(level.find('time_limit').text),
                    'board': []
                }
                board_element = level.find('board')
                if board_element is not None:
                    for row in board_element.findall('row'):
                        level_data['board'].append(
                            [int(cell) for cell in row.text.split()])
                levels.append(level_data)
            return levels
        except Exception as e:
            
            return []

    @staticmethod
    def load_jewels_config(filename: str) -> List[Dict]:
        try:
            tree = ConfigLoader.load_config(filename)
            root = tree.getroot()
            jewels = []
            for jewel in root.findall('jewel'):
                jewel_data = {
                    'id': int(jewel.get('id')),
                    'color': jewel.find('color').text,
                    'points': int(jewel.find('points').text),
                    'effect': jewel.find('effect').text if jewel.find('effect') is not None else None,
                    'image': jewel.find('image').text
                }
                jewels.append(jewel_data)
            return jewels
        except Exception as e:
            
            return []

    @staticmethod
    def load_high_scores(filename: str) -> List[Dict]:
        try:
            tree = ConfigLoader.load_config(filename)
            root = tree.getroot()
            scores = []
            for score in root.findall('score'):
                score_data = {
                    'name': score.find('name').text,
                    'points': int(score.find('points').text),
                    'level': score.find('level').text,
                    'mode': score.find('mode').text,
                    'date': score.find('date').text
                }
                scores.append(score_data)
            return sorted(scores, key=lambda x: int(
                x['points']), reverse=True)[:10]
        except Exception:
            return []

    @staticmethod
    def save_high_scores(filename: str, scores: List[Dict]):
        root = ET.Element('high_scores')
        for score in scores:
            score_elem = ET.SubElement(root, 'score')
            ET.SubElement(score_elem, 'name').text = score['name']
            ET.SubElement(score_elem, 'points').text = str(score['points'])
            ET.SubElement(score_elem, 'level').text = str(score['level'])
            ET.SubElement(score_elem, 'mode').text = score['mode']
            ET.SubElement(score_elem, 'date').text
        tree = ET.ElementTree(root)
        tree.write(filename)