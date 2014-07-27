"""
A solution to Question(code) attached with mail.

@author: Mayur Swami
@date: 26/07/2014
"""
from __future__ import division
import csv
from collections import Counter
from itertools import combinations_with_replacement
import sys

class ConferenceError(Exception):
    """
    A base exception to rase error for :class: `Conference`.
    """
    def __init__(self, message=""):
        self.message = message
        super(Exception, self).__init__(message)

    def __str__(self):
        return repr(self.message)


def possible_slot_durations(total_duration, slot_limit):
    """
    Returns all possible combinations with total duration as given.
    :param total_duration: Possible range of integers that can be present
                           in the combination. (1-8) -> [1,2,4,8]
    :type total_duration: int
    :param slot_limit: Number of integers in each slot.
    :type slot_limit: int
    :returns: all possible durations that together sums to total_duration.
    """
    return [comb for comb in combinations_with_replacement(
        range(1, total_duration + 1),
        r=slot_limit) if sum(comb) == total_duration]

def modify_data_format(data):
    tmp = []
    for d in data:
        if isinstance(d, list):
            data.remove(d)
            tmp.append(d)

    if all([isinstance(p, str) for p in data]):
        tmp.append(data)

    return tmp

class Conference(object):
    """
    Used to arrange a conference as per the question.
    """
    def __init__(self, slots, duration, conf_file):
        """
        :param slots: Total number of slots.
        :type slots: int
        :param duration: Total duration in hours
        :type duration: int
        :param conf_file: csv file from where data will be fetched as input.
        :type conf_file: str
        """
        self.slots = slots
        self.duration = duration
        self.conf_file = conf_file

    def _prep_data_from_csv(self):
        """
        Load the data from csv file and prepare it for evaluating.
        """
        durations = []
        presenters = []
        try:
            with open(self.conf_file, "rb") as f:
                csv_reader = csv.DictReader(f)
                for content in csv_reader:
                    durations.append(int(content['duration']))
                    presenters.append(content)
        except IOError:
            raise ConferenceError("Problem while opening csv file.")

        presenters = [{k: int(v) if k in ['cost', 'duration'] else v  for k,
                       v in pinfo.items()} for pinfo in presenters]

        return (durations, presenters)


    def _get_min_cost_n_presenter_by_duration(self, all_presenters,
                                              durationcount):
        """
        Calculate the cost for a possible combination of preseneter
        as specified by :param durationcount.
        :param all_presenters: list of dict containing info of all
                               registered presenters.
                               e.g., [{'name': 'p1', 'cost': '100',
                               'duration': '3'}, ..]
        :type all_presenters: list of dicts
        :param durationcount: count of durations e.g., {1: 3, 2: 2}
                        where key is the duration, and
                              value is the total count of duration as given
                              by input data or csv file.
        :type durationcount: dict
        :returns: tuple of total cost incurred for selecting a given set
                  of presenters and list of prseneters name.
        """
        ppresenters = []
        pcost = 0
        for duration, count in durationcount.items():
            #Sort in ascending order so that cost will go from min to max.
            presenters_by_duration = sorted([presenter
                                             for presenter in all_presenters
                                             if int(presenter['duration']) ==
                                             duration],
                                            key=lambda k: k['cost'])

            #return number of presenters(specified by count) having minimum cost
            ppresenters.extend([p['name'] for p
                                in presenters_by_duration[:count]])

            #Sum total cost by all the presenters.
            pcost += sum([p['cost'] for p in presenters_by_duration[:count]])
        return (pcost, ppresenters)


    def arrange_conf(self):
        """
        Arrange a confrence in 8 hours duration with exactly 3 slots.
        :returns: tuple containing list of selected_presenters and  their
        proposed cost.
        e.g., (['p2', 'p3', 'p4', 'p5'], 200)
        """
        (durations, presenters) = self._prep_data_from_csv()
        #Counter to hole number of duration counts.
        duration_count = Counter(durations)

        #Initially assign min_cost to some large value to ease on comparison.
        min_cost = sys.maxint
        selected_presenters = []
        finalist_presenters = []
        is_multi = False
        for i in xrange(self.duration, 0, -1):
            slot_durations = possible_slot_durations(self.duration, i)
            for sd in slot_durations:
                pcost = 0
                poss_presenters = []
                possible_combinations = Counter(sd)
                if all(duration in duration_count and
                       duration_count[duration] >= count
                       for duration, count in  possible_combinations.items()):
                       
                    (pcost, poss_presenters) = \
                            self._get_min_cost_n_presenter_by_duration(
                                presenters, possible_combinations)
                    
                    len_poss_presenters = len(poss_presenters)
                    len_selected_presenters = len(selected_presenters)
                    if pcost < min_cost:
                        if len_poss_presenters > len_selected_presenters:
                            selected_presenters = poss_presenters
                            min_cost = pcost
                        elif len_poss_presenters <= len_selected_presenters:
                            #if this case happens then we should first
                            #calculate the average cost per person
                            #Choose possible presenter over selected
                            #presennters
                            #if average cost of poss presenters is less than
                            #selected presenters
                            try:
                                avg_cost_poss = pcost/len_poss_presenters
                                avg_cost_selected = \
                                        min_cost/len_selected_presenters
                                if avg_cost_poss < avg_cost_selected:
                                    selected_presenters = poss_presenters
                                    min_cost = pcost
                            except ZeroDivisionError:
                                min_cost = pcost if len_poss_presenters > 0 \
                                           else min_cost
                                selected_presenters = poss_presenters \
                                        if len_poss_presenters > 0\
                                        else selected_presenters
                    elif pcost == min_cost:
                        #Also, select mutiple combination of presenters with
                        #same cost and maximum presenters
                        if len_poss_presenters == len_selected_presenters:
                            selected_presenters.append(poss_presenters)
                        elif len_poss_presenters > len_selected_presenters:
                            selected_presenters = poss_presenters

        if len(selected_presenters) == 0:
            raise ConferenceError("Not enough presenters.")

        selected_presenters = modify_data_format(selected_presenters)
        return (selected_presenters, min_cost)



if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
    except IndexError:
        input_file = "test_file.csv"
    conf = Conference(3, 8, input_file)

    (selected_presenters, cost) = conf.arrange_conf()
    selected_presenters = [str(p) for p in selected_presenters]
    print "Following are selected presenters {} "\
               "with incurred cost: {}".format(",".join(selected_presenters),
                                               cost)


