import numpy as np
import pandas as pd

# Define constants
NUM_TEACHERS = 10
NUM_PERIODS_PER_WEEK = 30
NUM_DAYS_PER_WEEK = 5
NUM_CLASSES = 50
NUM_GENERATIONS = 100
MUTATION_RATE = 0.1
NUM_PARENTS = 2
POPULATION_SIZE = 50

# Define hard constraints
NO_TWO_CLASSES_AT_SAME_TIME = lambda x: len(set(x)) == len(x)
NO_THREE_CONSECUTIVE_CLASSES = lambda x: all([len(list(g))<3 for k,g in itertools.groupby(x)])
NO_CLASS_BEFORE_8_30_AM = lambda x: all([p >= 2 for p in x])
NO_CLASS_AFTER_5_PM = lambda x: all([p <= 21 for p in x])
NO_CLASSES_ON_WEEKENDS = lambda x: not any([(p%NUM_PERIODS_PER_WEEK)%NUM_DAYS_PER_WEEK > 4 for p in x])
NO_DUPLICATE_CLASSROOMS = lambda x: len(set([c[1] for c in x])) == len(x)
NO_DUPLICATE_TEACHERS = lambda x: len(set([c[2] for c in x])) == len(x)
NO_DUPLICATE_SECTIONS = lambda x: len(set([c[3] for c in x])) == len(x)
HARD_CONSTRAINTS = [NO_TWO_CLASSES_AT_SAME_TIME, NO_THREE_CONSECUTIVE_CLASSES,
                    NO_CLASS_BEFORE_8_30_AM, NO_CLASS_AFTER_5_PM, NO_CLASSES_ON_WEEKENDS,
                    NO_DUPLICATE_CLASSROOMS, NO_DUPLICATE_TEACHERS, NO_DUPLICATE_SECTIONS]

# Define soft constraints
NO_CLASS_FROM_1_TO_2_ON_FRIDAY = lambda x: all([p%NUM_PERIODS_PER_WEEK%NUM_DAYS_PER_WEEK!=3 or (p%NUM_PERIODS_PER_WEEK)/NUM_DAYS_PER_WEEK!=1 for p in x])
NO_THREE_CONSECUTIVE_SECTIONS = lambda x: all([len(list(g))<3 for k,g in itertools.groupby([c[3] for c in x])])
PREFERRED_ORDER_FOR_SUBJECTS = lambda x: all([True if x[i][0] != x[i+1][0] or (x[i][0] == x[i+1][0] and x[i][4] == 'lecture' and x[i+1][4] == 'lab') else False for i in range(len(x)-1)])
ONE_HOUR_FACULTY_MEETING = lambda x: len([p for p in x if p%NUM_PERIODS_PER_WEEK%NUM_DAYS_PER_WEEK!=2]) >= 1
SOFT_CONSTRAINTS = [NO_CLASS_FROM_1_TO_2_ON_FRIDAY, NO_THREE_CONSECUTIVE_SECTIONS,
                    PREFERRED_ORDER_FOR_SUBJECTS, ONE_HOUR_FACULTY_MEETING]

def generate_population(num_classes):
    population = []
    for i in range(POPULATION_SIZE):
        class_schedule = []
        for j in range(num_classes):
            teacher = np.random.randint(NUM_TEACHERS)
            period = np.random.randint(NUM_PERIODS_PER_WEEK)
            day = period % NUM_DAYS_PER_WEEK
            section = np.random.randint(NUM_SECTIONS)
            classroom = np.random.randint(NUM_CLASSROOMS)
            class_schedule.append((teacher, classroom, section, period, 'lecture'))
            lab_period = (period+1)%NUM_PERIODS_PER_WEEK if day<NUM_DAYS_PER_WEEK-1 else (period-NUM_DAYS_PER_WEEK+1)%NUM_PERIODS_PER_WEEK
            if course_data['lab_slot'][day][lab_period] == 0:
                course_data['lab_slot'][day][lab_period] = 1
                new_chromosome[i]['lab_day'][period] = day
                new_chromosome[i]['lab_period'][period] = lab_period
                break
    return new_chromosome

def fitness_function(chromosome):
    fitness = 0
    # Calculate fitness for hard constraints
    # No teacher can hold two classes at the same time
    for i in range(NUM_TEACHERS):
        for day in range(NUM_DAYS_PER_WEEK):
            for period in range(NUM_PERIODS_PER_DAY):
                course_indices = [index for index, c in enumerate(chromosome) if c['teacher'] == i]
                course_indices_same_time = [index for index in course_indices if chromosome[index]['day'][period] == day and chromosome[index]['period'][period] == period]
                if len(course_indices_same_time) > 1:
                    fitness -= 1

# No section can listen for two classes at the same time
    for i in range(NUM_SECTIONS):
        for day in range(NUM_DAYS_PER_WEEK):
            for period in range(NUM_PERIODS_PER_DAY):
                course_indices = [index for index, c in enumerate(chromosome) if c['section'] == i]
                course_indices_same_time = [index for index in course_indices if chromosome[index]['day'][period] == day and chromosome[index]['period'][period] == period]
                if len(course_indices_same_time) > 1:
                    fitness -= 1

# No classroom can receive two classes at the same time
    for i in range(NUM_CLASSROOMS):
        for day in range(NUM_DAYS_PER_WEEK):
            for period in range(NUM_PERIODS_PER_DAY):
                course_indices = [index for index, c in enumerate(chromosome) if c['classroom'] == i]
                course_indices_same_time = [index for index in course_indices if chromosome[index]['day'][period] == day and chromosome[index]['period'][period] == period]
                if len(course_indices_same_time) > 1:
                    fitness -= 1

# No teacher can hold three consecutive classes
    for i in range(NUM_TEACHERS):
        for day in range(NUM_DAYS_PER_WEEK):
            for period in range(NUM_PERIODS_PER_DAY-2):
                course_indices = [index for index, c in enumerate(chromosome) if c['teacher'] == i]
                course_indices_same_time = [index for index in course_indices if chromosome[index]['day'][period] == day and chromosome[index]['period'][period] == period]
                course_indices_same_time_next1 = [index for index in course_indices if chromosome[index]['day'][period+1] == day and chromosome[index]['period'][period+1] == period+1]
                course_indices_same_time_next2 = [index for index in course_indices if chromosome[index]['day'][period+2] == day and chromosome[index]['period'][period+2] == period+2]
                if len(course_indices_same_time) > 0 and len(course_indices_same_time_next1) > 0 and len(course_indices_same_time_next2) > 0:
                    fitness -= 1

# There will be no class before 8:30 am and after 5:00 pm
    for i in range(NUM_COURSES):
        for period in range(NUM_PERIODS_PER_WEEK):
            if (chromosome[i]['day'][period] < NUM_DAYS_PER_WEEK-1 and chromosome[i]['period'][period] < 2) or (chromosome[i]['day'][period] == NUM_DAYS_PER_WEEK-1 and chromosome[i]['period'][period] == 0):
                if chromosome[i]['type'] == 'lecture':
                    lab_period = (period+1)%NUM_PERIODS_PER_WEEK if chromosome[i]['day'][period] < NUM_DAYS_PER_WEEK-1 else (period-NUM_DAYS_PER_WEEK+1)
                    if (chromosome[i]['teacher'], chromosome[i]['section'], chromosome[i]['course'], lab_period) in unavailable_slots:
                        return False
                elif chromosome[i]['type'] == 'lab':
                    lecture_period = (period-1)%NUM_PERIODS_PER_WEEK if chromosome[i]['day'][period] < NUM_DAYS_PER_WEEK-1 else (period-NUM_DAYS_PER_WEEK-1)
                    if (chromosome[i]['teacher'], chromosome[i]['section'], chromosome[i]['course'], lecture_period) in unavailable_slots:
                        return False
        if consecutive_count > 2:
            return False
        if chromosome[i]['day'][0] == NUM_DAYS_PER_WEEK-1 and chromosome[i]['period'][0] == 3:
            if (chromosome[i]['teacher'], 'faculty meeting') in unavailable_slots:
                return False
        if chromosome[i]['day'][0] == NUM_DAYS_PER_WEEK-1 and chromosome[i]['period'][0] == 4:
            if (chromosome[i]['teacher'], 'prayer break') in unavailable_slots:
                return False
    return True