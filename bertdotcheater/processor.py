from bertdotcheater.ascii import AsciiColors
from bertdotcheater.logger import Logger
import os
import io
import re
import itertools
import sys

colors = AsciiColors()
# Initialize logging facility
logger = Logger().init_logger('processor')

class CheatFileProcessor:

  def __init__(self, **kwargs):
    # Parse parameters
    search_topics = kwargs['topics']
    condition = 'any' if kwargs['any'] else 'all'
    # Build regular expression
    search_list = []
    no_pause = kwargs.get('no_pause')
    self.search_body = True if kwargs['search_body'] else False
    self.pause = False if kwargs['no_pause'] else True
    self.explode = kwargs.get('explode')
    # Warn if search body is enabled
    if self.search_body:
        logger.warning('Search includes cheat body; can\'t yet reliably determine count of matched topics')
    if condition == 'all':
        regx = '.*%s'
        # Account for ALL permutations of the list of search topics
        search_permutations = list(itertools.permutations(list(search_topics)))
        for sp in search_permutations:
            search_list.append('(%s)|' % ''.join([regx % p for p in sp]))
        search = ''.join(search_list)
    else:
        regx = '.*%s|'
        search = ''.join([regx % t for t in search_topics])
    self.search = re.sub('\|$', '', search)
    logger.debug('Regular expression is: %s' % search)
    # Compile the regular expression
    self.string = re.compile(search)
    self.matched_topics = []

  def process_cheat_file(self, cheatfile):
    if os.path.exists(cheatfile) and not os.path.isdir(cheatfile):
        try:
            with io.open(cheatfile, "r", encoding="utf-8") as n:
                cheats = n.readlines()
        except UnicodeDecodeError:
            try:
                with io.open(cheatfile, "r") as n:
                    cheats = n.readlines()
            except Exception:
                print()
        cheats_length = len(cheats)
        topics = [(i, n) for i, n in enumerate(cheats) if n.startswith('# ')]
        for index, line in enumerate(topics):
            # Find the corresponding line index
            s_line_index = topics[index][0]
            # Skip topics not matching search term (if applicable)
            cheat_topic = cheats[s_line_index]
            match_length = len(self.string.search(cheat_topic).group()) if self.string.search(cheat_topic) else []
            if not any([match_length, self.search_body]):
                continue
            if not self.search_body:
                logger.info(f'Topic search criteria matched against cheat file: {colors.emerald(cheatfile)}')
            # Find the next corresponding line index
            s_next_line_index = cheats_length if index + 1 > len(topics) - 1 else topics[index + 1][0]
            # Grab the topic headers
            header_list = ['# %s' % header.strip() for header in cheat_topic.split('# ') if header]
            headers = ' '.join(sorted(set(header_list), key=header_list.index))
            # headers = '# %s' % ' # '.join([h for h in headers])
            # Get the topic's body
            body = ''.join([l for l in cheats[s_line_index + 1:s_next_line_index] if l])
            body_matched_strings = self.string.search(body) if self.search_body else None
            if not any([self.string.search(cheat_topic), body_matched_strings]):
                continue
            try:
                if self.search_body:
                    body = body_matched_strings.group().encode('utf-8')
            except Exception:
                logger.error('Failed to search body for this topic: {c}'.format(
                    c=colors.red(cheat_topic)))
            # utf-8 encoding
            try:
                headers = str(headers.encode('utf-8').decode('utf8'))
                body = str(body.encode('utf-8').decode('utf8'))
            except UnicodeEncodeError:
                try:
                    body = str(body.encode('utf-8'))
                except Exception:
                    logger.error('I had trouble encoding this topic: {c}'.format(
                        c=colors.red(cheat_topic)))
                    continue
            if self.explode:
                output_filename = re.sub("\s|#|:|/|'", "_", headers.split('#')[1].strip()) + '.md'
                try:
                    with io.open(output_filename, "a", encoding="utf-8") as text_file:
                        print("{h}\n{b}".format(h=colors.purple(headers), b=colors.green(body)))
                        text_file.write("{h}\n{b}".format(h=headers, b=body))
                        self.matched_topics.append(headers)
                    if self.pause:
                        wait = input("PRESS ENTER TO CONTINUE TO NEXT TOPIC or 'q' to quit ")
                        if wait.lower() == 'q':
                            sys.exit()
                except Exception:
                    logger.error('Failed to write {h} ... skipping'.format(h=headers))
            else:
                try:
                    print('{h}\n{b}'.format(h=colors.purple(headers), b=colors.green(body)))
                    self.matched_topics.append(headers)
                    if self.pause:
                        wait = input("ENTER => CONTINUE TO NEXT TOPIC or 'q' to quit ")
                        if wait.lower() == 'q':
                            sys.exit()                            
                except Exception:
                    logger.error('Failed to process topic ... skipping')
                    continue