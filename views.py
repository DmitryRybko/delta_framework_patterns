from delta_framework.templator import render
from creational_patterns import Engine, MapperRegistry
# from urls import routes
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, \
    ListView, CreateView, BaseSerializer
from debug import Debug, DebugAlt, DebugNew
from route_deco import AppRoute
from architectural_system_pattern_unit_of_work import UnitOfWork
routes = {}

site = Engine()
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@AppRoute(routes=routes, url='/')
class Index:
    @Debug("Index")
    def __call__(self, request):
        return '200 OK', render('index.html')


@AppRoute(routes=routes, url='/courses/')
class Courses:
    @DebugAlt("Courses")
    def __call__(self, request):
        return '200 OK', render('courses.html', objects_list=site.courses)


@AppRoute(routes=routes, url='/about/')
class About:
    @DebugNew()
    def __call__(self, request):
        return '200 OK', render('about.html')


@AppRoute(routes=routes, url='/contact/')
class Contact:
    @DebugNew()
    def __call__(self, request):
        return '200 OK', render('contact.html')


@AppRoute(routes=routes, url='/createcategory/')
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name)

            site.categories.append(new_category)
            new_category.mark_new()
            UnitOfWork.get_current().commit()

            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


@AppRoute(routes=routes, url='/categorylist/')
class CategoryList(ListView):

    queryset = site.categories
    template_name = 'category_list.html'
    # def __call__(self, request):
    #     print(site.categories)
    #     return '200 OK', render('category_list.html', objects_list=site.categories)

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('category')
        return mapper.all()


@AppRoute(routes=routes, url='/createcourse/')
class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']
            print(request)
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = MapperRegistry.get_current_mapper("category").find_by_id(int(self.category_id))

                course = site.create_course('online', name, category)

                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)

                site.courses.append(course)

            return '200 OK', render('courses.html', objects_list=site.courses,
                                    name=category.name)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                print(request)
                category = MapperRegistry.get_current_mapper("category").find_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', name=category.name)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()