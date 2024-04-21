from service.auth.models import UserModel

class SearchModel():
    __search_data__ = UserModel().get_users()
    def get_search_data(self):
        return self.__search_data__