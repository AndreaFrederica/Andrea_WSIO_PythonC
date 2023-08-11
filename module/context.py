import module

context = None

route_func_list:list = list()
routes:dict = dict()
modules:dict = dict()
route2module:dict = dict()                #! 路由转模块名
func2module:dict = dict()
route2funcs:dict = dict()
registered_funcs:list = list()
func_full_name2func_name:dict() = dict()

event_func_list:list = list()
events:dict = dict()
event2module:dict = dict()

timers = list()
timer_info = dict()

flag_exit = False
main_exit_flag = False

all_mc_sessions = dict()
all_cq_sessions = dict()