const DOMAIN_ROOT = '/learn/domain';
const GET_DOMAINS_API = DOMAIN_ROOT  + '/list';
const GET_USER_DOMAINS_API = DOMAIN_ROOT + '/list/user'
const GET_DOMAIN_TREE = DOMAIN_ROOT + '/tree'

get_domains = () => req(GET_DOMAINS_API)();
get_user_domains = (user_id) => req(GET_USER_DOMAINS_API)(user_id);
get_domain_tree = (domain_id) => req(GET_DOMAIN_TREE)(domain_id);
