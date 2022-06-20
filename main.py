from API_classes.GUI_class import Graphics
# from API_classes.Data_classifier_class import Data_clasffier
class Main():
    # Funcion para inciar el modo GUI de la aplicacion
    def init_GUI(self):
        self.gui = Graphics()


# Data_clasffier().fix_dictionary_date()
# Data_clasffier().store_inital_data()
# Data_clasffier().update_data("Classified_By_BgpRS.json")
# Data_clasffier().load_bgp_issues_from_file("BGP_TFM/dataset/partial_record.json","final_dict_by_country_maximi_v3.json")
Main().init_GUI()
