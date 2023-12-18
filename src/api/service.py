from src.api.schemas import Resume, Vacancy, SalaryType, EducationType


class MatchingService:
    @staticmethod
    def salary_type_match(resume: Resume, vacancy: Vacancy) -> bool:
        if resume.salary_type == vacancy.salary_type == SalaryType.range:
            return (
                    vacancy.min_value <= resume.min_value <= vacancy.max_value
                    or
                    vacancy.min_value <= resume.max_value <= vacancy.max_value
            )
        elif resume.salary_type == SalaryType.range and vacancy.salary_type == SalaryType.value:
            return resume.min_value <= vacancy.value <= resume.max_value
        elif resume.salary_type == SalaryType.value and vacancy.salary_type == SalaryType.range:
            return vacancy.min_value <= resume.value <= vacancy.max_value
        elif resume.salary_type == vacancy.salary_type == SalaryType.value:
            return resume.value == vacancy.value
        elif resume.salary_type == vacancy.salary_type == SalaryType.no:
            return True
        else:
            return False

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
    def match(resume: Resume, vacancy: Vacancy) -> float:
        city_match = resume.city == vacancy.city
        employment_match = any(e_type in vacancy.employment for e_type in resume.employment)
        education_match = MatchingService.education_match(resume.education, vacancy.education)
        schedule_match = any(sh_type in vacancy.schedule for sh_type in resume.schedule)
        move_match = resume.move == vacancy.move
        salary_type_match = MatchingService.salary_type_match(resume, vacancy)
        if not all ([city_match, employment_match, education_match, schedule_match, move_match, salary_type_match]):
            return 0
        else:
            return 100 * MatchingService.simply_similarity(resume.name, vacancy.name)
