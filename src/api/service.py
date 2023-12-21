from src.api.schemas import Resume, Vacancy, SalaryType, EducationType, MoveType
import math

class MatchingService:

    @staticmethod
    def find_move_correspondance(resume_move:MoveType, vacancy_move:MoveType, resume_city:str, vacancy_city: str):
        if resume_city!=vacancy_city:
            if vacancy_move==MoveType.no or resume_move==MoveType.no:
                return 0
            elif resume_move==MoveType.may_be and vacancy_move==MoveType.may_be:
                return 0.5
            else:
                return 1
        else:
            if resume_move == MoveType.yes and vacancy_move == MoveType.yes:
                return 0.25
            elif resume_move == MoveType.yes or vacancy_move == MoveType.yes:
                return 0.5
            else:
                return 1

    @staticmethod
    def find_salary_correspondance(vacancy_salary: float, cv_salary: float) -> float:
        if (2*vacancy_salary<cv_salary):
            return -1
        elif (2*cv_salary<vacancy_salary):
            return 1
        else:
            return (vacancy_salary-cv_salary)/min(cv_salary, vacancy_salary)


    @staticmethod
    def salary_type_match(resume: Resume, vacancy: Vacancy) -> float:
        if resume.salary_type == vacancy.salary_type == SalaryType.range:
            return MatchingService.find_salary_correspondance(vacancy.max_value, resume.max_value)
        elif resume.salary_type == SalaryType.range and vacancy.salary_type == SalaryType.value:
            return MatchingService.find_salary_correspondance(vacancy.value, resume.max_value)
        elif resume.salary_type == SalaryType.value and vacancy.salary_type == SalaryType.range:
            return MatchingService.find_salary_correspondance(vacancy.max_value, resume.value)
        elif resume.salary_type == vacancy.salary_type == SalaryType.value:
            return MatchingService.find_salary_correspondance(vacancy.value, resume.value)
        return 0


    @staticmethod
    def education_match(resume_education: EducationType, vacancy_education: EducationType) -> bool:
        if resume_education == vacancy_education:
            education_match = True
        elif resume_education == EducationType.high and (
            vacancy_education == EducationType.almost_high
            or vacancy_education == EducationType.middle_special
            or vacancy_education == EducationType.middle
        ):
            education_match = True
        elif resume_education == EducationType.almost_high and (
            vacancy_education == EducationType.middle_special
            or vacancy_education == EducationType.middle
        ):
            education_match = True
        elif (
            resume_education == EducationType.middle_special
            and vacancy_education == EducationType.middle
        ):
            education_match = True
        else:
            education_match = False
        return education_match

    @staticmethod
    def simply_similarity(name1: str, name2: str) -> float:
        tokens1 = name1.lower().split()
        tokens2 = name2.lower().split()
        n_inner = len(set(tokens1).intersection(set(tokens2)))
        if len(tokens1) == len(tokens2) == 0:
            return 0
        return n_inner / max(len(tokens1), len(tokens2))

    @staticmethod
    def ml_similarity(word1: str, word2: str, model) -> float:
        print(model.find_similarity(word1, word2))
        return model.find_similarity(word1, word2)

    @staticmethod
    def match(resume: Resume, vacancy: Vacancy, model) -> float:
        employment_match = any(e_type in vacancy.employment for e_type in resume.employment)
        education_match = MatchingService.education_match(resume.education, vacancy.education)
        schedule_match = any(sh_type in vacancy.schedule for sh_type in resume.schedule)
        move_match = MatchingService.find_move_correspondance(resume.move, vacancy.move,
                                                              resume.city, vacancy.city)
        salary_type_match = MatchingService.salary_type_match(resume, vacancy)
        if not all ([employment_match, education_match, schedule_match, move_match]):
            return 0
        else:
            return max(0, 70 * MatchingService.ml_similarity(resume.name, vacancy.name, model)
                       + 20 * salary_type_match + 10*move_match)
