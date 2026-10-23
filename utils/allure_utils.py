import allure
def allure_init(case):
    allure.dynamic.feature(case.get("feature", "未分类"))
    allure.dynamic.story(case.get("story", "未分类"))
    allure.dynamic.title(f"ID:{case.get('id', '未分类')}--{case.get('title', '未分类')}")