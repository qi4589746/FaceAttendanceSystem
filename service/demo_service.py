import repository.subject_rep as subjectRep
from agent import time_generator as tg
from domain.subject import Subject


def _initializationDatabase():
    subject = Subject('demoSubject', 'demoSubject', tg.getNowAsMilli(), tg.getNowAsMilli())
    if subjectRep.findById(subject.id) is None:
        print('Create demo subject.')
        subjectRep.save(subject)
