const API_ROOT = '/api'
const DOMAIN_ROOT = API_ROOT + '/learn/domain';
const SECTION_ROOT = API_ROOT + '/learn/section';
const NODE_ROOT = API_ROOT + '/learn/node';


const GET_DOMAINS_API = DOMAIN_ROOT  + '/list';
const GET_USER_DOMAINS_API = DOMAIN_ROOT + '/user/list';
const GET_DOMAIN_TREE_API = DOMAIN_ROOT + '/tree';
const GET_LOGS_API = DOMAIN_ROOT + '/log'

const GET_SECTION_API = SECTION_ROOT
const GET_SECTION_TREE_API = SECTION_ROOT + '/tree'

const GET_NODE_API = NODE_ROOT
const GET_MATERIALS_API = NODE_ROOT + '/materials';



get_domains = () => req(GET_DOMAINS_API)();
get_domain = (domain_id) => req(GET_DOMAINS_API)(domain_id);
get_user_domains = () => req(GET_USER_DOMAINS_API)();
get_user_domain = (domain_id) => req(GET_USER_DOMAINS_API)(domain_id);
get_domain_tree = (domain_id) => req(GET_DOMAIN_TREE_API)(domain_id);
get_logs = () => req(GET_LOGS_API)();
get_domain_logs = (domain_id) => req(GET_LOGS_API)(domain_id);

get_section = (section_id) => req(GET_SECTION_API)(section_id);
get_section_tree = (section_id) => req(GET_SECTION_TREE_API)(section_id);

get_node = (node_id) => req(GET_NODE_API)(node_id);
get_materials = (node_id) => req(GET_MATERIALS_API)(node_id);
