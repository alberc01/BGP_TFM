from API_classes.BGP_class import BGP
import API_classes.utils as ut
# TODO Limpiar comentarios y codigo de Debug
class PR_BGP(BGP):
    
    def __init__(self, country_data, country_iso2, raw_data, ot_data, o_date, r_date):
        super().__init__(country_data, country_iso2, raw_data, ot_data, o_date, r_date)
        self.selected_list = []
        self.asn_data = self.get_ASN_info_to_recommend()
        self.mainlist = self.set_mainlist()
    
    def set_mainlist(self):
        mainlist = []
        for i in self.asn_data.keys():
            if i not in mainlist:
                mainlist.append(str(i))
        return mainlist
        
    def add_to_selected_list(self, v):
        if (v != "") and (v not in self.selected_list):
            self.selected_list.append(v)

    def set_selected_list(self,list):
        self.selected_list = list.copy()

    def remove_from_selected_list(self, v):
        if v in self.selected_list:
            self.selected_list.remove(v)
    
    def clear_selected_list(self):
        self.selected_list = []

    def get_selected_list(self):
        return self.selected_list

    def get_correct_asn(self, list):
        for item in list:
            if item.replace('AS','').isnumeric():
                return item
            else:
                print(item + " is not valid")

    def get_ASN_info_to_recommend(self):
        asn_dict = {}
        for primary_k in self.raw_data.keys():
            if primary_k != 'oldest_date' and primary_k != 'most_recent_date':

                # Informacion ASN para los outages
                for k,v in self.raw_data[primary_k]['OT_by_date'].items():
                    for item in v:
                        asn_key = item['ASN']
                        asn_cntry = item['ctry']
                        
                        important_Data = item['scrapped_from_url']

                        if  asn_key not in asn_dict.keys():
                            asn_dict[asn_key] = {
                                'dates_ot': [k],
                                'dates_hj': [],
                                'country': asn_cntry,
                                'moredetail': important_Data            
                                }
                        else:
                            asn_dict[asn_key]['dates_ot'].append(k)
                            asn_dict[asn_key]['moredetail'] = important_Data

                # TODO ¿Hace falta utilizar la informacon de los AS que son perjudicados en Hijack para las funciones de recomendacion?
                # Informacion ASN para los hijacks perjudicados
                # for k,v in self.raw_data[primary_k]['HJ_by_date']['injured'].items():
                #     for item in v:
                #         asn_inj_ctry = item['ctry_inj']
                #         asn_cau_ctry = item['ctry_cau']
                #         asn_cau_key = self.get_correct_asn(item['ASN_cau'])
                #         asn_inju_key = self.get_correct_asn(item['ASN_inj'])

                #         important_Data = item['scrapped_from_url']
                
                #         if asn_inju_key not in asn_dict.keys():
                #             asn_dict[asn_inju_key] = {
                #                 'dates_ot': [],
                #                 'dates_hj': [k],
                #                 'country': asn_inj_ctry,
                #                 'moredetail': important_Data               
                #                 }
                #         else:
                #             asn_dict[asn_inju_key]['dates_hj'].append(k)
                #             asn_dict[asn_inju_key]['moredetail'] = important_Data

                #         if asn_cau_key not in asn_dict.keys():
                #             asn_dict[asn_cau_key] = {
                #                 'dates_ot': [],
                #                 'dates_hj': [k],
                #                 'country': asn_cau_ctry,
                #                 'moredetail': important_Data              
                #                 }
                #         else:
                #             asn_dict[asn_cau_key]['dates_hj'].append(k)
                #             asn_dict[asn_cau_key]['moredetail'] = important_Data
        
                # Informacion ASN para los hijacks causantes
                for k,v in self.raw_data[primary_k]['HJ_by_date']['causer'].items():
                    for item in v:
                        asn_cau_key = self.get_correct_asn(item['ASN_cau'])
                        asn_inju_key = self.get_correct_asn(item['ASN_inj'])
                        asn_cau_ctry = item['ctry_cau']
                        asn_inj_ctry = item['ctry_inj']
                        important_Data = item['scrapped_from_url']

                        if asn_inju_key not in asn_dict.keys():
                            asn_dict[asn_inju_key] = {
                                'dates_ot': [],
                                'dates_hj': [k],
                                'country': asn_inj_ctry,
                                'moredetail': important_Data               
                                }
                        else:
                            asn_dict[asn_inju_key]['dates_hj'].append(k)
                            asn_dict[asn_inju_key]['moredetail'] = important_Data

                        if asn_cau_key not in asn_dict.keys():
                            asn_dict[asn_cau_key] = {
                                'dates_ot': [],
                                'dates_hj': [k],
                                'country': asn_cau_ctry,
                                'moredetail': important_Data               
                                }
                        else:
                            asn_dict[asn_cau_key]['dates_hj'].append(k)
                            asn_dict[asn_cau_key]['moredetail'] = important_Data
                
                # TODO Mirar que hacer con los secuestros con origen y destino identicos
                # for k,v in self.raw_data['HJ_autosabotage'].items():

        return asn_dict

    #TODO Hacer tendencias
    def get_recomendation_HJ(self, hj_results, asn_cau):
        max_incidents = 3
        incident_count = 0
        local_pref_factor = 10
        for item in hj_results:
            if item >= max_incidents:
                incident_count+=1
        
        pref_to_reduce = incident_count*local_pref_factor
        commands = self.construct_vtysh_commands_hj(asn_cau, pref_to_reduce)
        return pref_to_reduce,commands
                

    def get_recomendation_OT(self, ot_results, asn_cau):
        max_incidents = 3
        incident_count = 0
        local_pref_factor = 5
        for item in ot_results:
            if item >= max_incidents:
                incident_count+=1
        
        pref_to_reduce = incident_count*local_pref_factor
        commands = self.construct_vtysh_commands_ot(asn_cau, pref_to_reduce)
        return pref_to_reduce,commands

    # Funcion para evaluar los secuestros
    def get_HJ_evaluation(self, asn_selected):
        asn_hj = self.get_incidents_by_month(self.asn_data[asn_selected]['dates_hj'])
        return asn_hj

    # Funcion para evaluar las caidas de servicio
    def get_OT_evaluation(self, asn_selected):
        asn_ot = self.get_incidents_by_month(self.asn_data[asn_selected]['dates_ot'])
        return asn_ot
    
    def get_incidents_by_month(self, data):
        # Obtener el numero de caidas al mes
        if len(data) > 0:
            data.sort()
            month_constant = 30
            window_size = ut.string_to_datetime(data[-1]) - ut.string_to_datetime(data[0])
            window_size = int((window_size.days)/month_constant)+1
            evaluation = [0]*window_size
            month_idx = 0
            date_out = ut.string_to_datetime(data[0])
            first_date = date_out
            evaluation[month_idx] += 1 
            for i in range(1,len(data)):
                date_out_next = ut.string_to_datetime(data[i])
                date_diff = date_out_next - date_out
                if date_diff.days <= month_constant:
                    evaluation[month_idx] += 1 
                else:
                    date_out = date_out_next
                    total_time = date_out - first_date
                    month_idx = int(total_time.days/30)                  
                    evaluation[month_idx] += 1 

            return evaluation
        else:
            return data


    def construct_vtysh_commands_ot(self, asn, pref):
        # El filtrado solo debe contemplar aquellos anuncion en los que el asn esta en medio del AS_PATH
        asn_filter = '_'+ asn.replace('AS','')  + '_'
        string = "\
! Router section   \n\
router bgp <YOUR ASN NUMBER> \n\
    ! <a.b.c.d> is the IP direction of the router BGP neighbour\n\
    neighbor <a.b.c.d> remote_as " + asn.replace('AS','') + "\n\
    neighbor <a.b.c.d> route-map BgpRS_RM " + asn.replace('AS','')  + " in \n\
! Access-list declaration section \n\
ip access-list BgpRS_RECOM permit "+ asn_filter+ " !Filter to find all routes in AS_PATH where the AS problem causer is between \n\
! Route-map declaration section \n\
route-map BgpRS_RM permit 10 \n\
    match as-path BgpRS_RECOM\n\
    set local-prefence (- " + str(pref)+ ")" 
        return string
    

    def construct_vtysh_commands_hj(self, asn, pref):
        # El filtrado solo debe contemplar aquellos anuncios en los que el ASN es origen o final
        asn_filter = asn.replace('AS','') + '$' # Rutas con origen en el ASN agresor
        string = "\
! Router section   \n\
router bgp <YOUR ASN NUMBER> \n\
    ! <a.b.c.d> is the IP direction of the router BGP neighbour\n\
    neighbor <a.b.c.d> remote_as " + asn.replace('AS','') + "\n\
    neighbor <a.b.c.d> route-map BgpRS_RM " + asn.replace('AS','') + " in \n\
! Access-list declaration section \n\
ip access-list BgpRS_RECOM permit "+ asn_filter + " ! Filter to find all routes in AS_PATH where the AS problem is origin \n\
! Route-map declaration section \n\
route-map BgpRS_RM permit 10 \n\
    match as-path BgpRS_RECOM\n\
    set local-prefence (- " + str(pref)+ ")" 
        return string
