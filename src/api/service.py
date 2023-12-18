from src.api.schemas import Resume, Vacancy, SalaryType, EducationType


class MatchingService:
    @staticmethod
    def salary_type_match(resume: Resume, vacancy: Vacancy, find_similar_job=0.5) -> float:
        if resume.salary_type == vacancy.salary_type == SalaryType.range:
            return find_similar_job * 0.8 + vacancy.max_value / resume.max_value * 0.2
        elif resume.salary_type == SalaryType.range and vacancy.salary_type == SalaryType.value:
            return find_similar_job * 0.8 + vacancy.value / resume.max_value * 0.2
        elif resume.salary_type == SalaryType.value and vacancy.salary_type == SalaryType.range:
            return find_similar_job * 0.8 + vacancy.max_value / resume.value * 0.2
        elif resume.salary_type == vacancy.salary_type == SalaryType.value:
            return find_similar_job * 0.8 + vacancy.value / resume.value * 0.2
        else:
            return find_similar_job * 0.8

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
    def match(resume: Resume, vacancy: Vacancy) -> float:
        city_match = resume.city in vacancy.city

        employment_match = any(e_type in vacancy.employment for e_type in resume.employment)

        education_match = MatchingService.education_match(resume.education, vacancy.education)

        schedule_match = any(sh_type in vacancy.schedule for sh_type in resume.schedule)

        move_match = resume.move == vacancy.move

        if not (
            city_match and employment_match and education_match and schedule_match and move_match
        ):
            return 0
        else:
            return MatchingService.salary_type_match(resume, vacancy)
