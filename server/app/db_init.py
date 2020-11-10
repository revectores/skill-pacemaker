from app.models import *


def db_init():
	db.drop_all()
	db.create_all()
	users = [
	    User(id=1, username="1", password_hash="pbkdf2:sha256:150000$KSC58uVd$9ff4385d31b398a8d1f0b4fee34df4589dc75f7c24d067c2d203cdb9233d182f", email="1@qq.com")
	]

	domains = [
	    # Domain(id=1, name="测试领域", description="测试领域", tree_file="test.tree"),
	    Domain(id=1, name="Python", description="Python变量、函数、数据结构、流程控制、面向对象机制"),
	    Domain(id=2, name="C", description="C变量、函数、流程控制"),
	    Domain(id=3, name="编码", description="整数、浮点数、字符的编码方式") 
	]

	sections = [
	    Section(id=1, domain_id=1, name="variable"),
	    Section(id=2, domain_id=1, name="io"),
	    Section(id=3, domain_id=1, name="function"),
	    Section(id=4, domain_id=1, name="flow_control"),
	    Section(id=5, domain_id=1, name="native_datatype"),
	    Section(id=6, domain_id=1, name="module"),
	    Section(id=7, domain_id=1, name="oop")
	    # Section(domain_id=3, name="")
	]

	section_links = [
	    SectionLink(domain_id=1, source=1, target=3),
	    SectionLink(domain_id=1, source=1, target=4),
	    SectionLink(domain_id=1, source=1, target=5),
	    SectionLink(domain_id=1, source=2, target=3),
	    SectionLink(domain_id=1, source=2, target=4),
	    SectionLink(domain_id=1, source=2, target=5),
	    SectionLink(domain_id=1, source=3, target=6),
	    SectionLink(domain_id=1, source=3, target=7),
	    SectionLink(domain_id=1, source=5, target=7),
	]

	nodes = [
	    Node(id=1, section_id=1, name="variable_assignment"),
	    Node(id=2, section_id=1, name="constant"),
	    Node(id=3, section_id=2, name="print"),
	    Node(id=4, section_id=2, name="input"),
	    Node(id=5, section_id=3, name="function"),
	    Node(id=6, section_id=4, name="if"),
	    Node(id=7, section_id=4, name="for"),
	    Node(id=8, section_id=4, name="while"),
	    Node(id=9, section_id=5, name="int"),
	    Node(id=10, section_id=5, name="string"),
	    Node(id=11, section_id=5, name="float"),
	    Node(id=12, section_id=5, name="list"),
	    Node(id=13, section_id=5, name="tuple"),
	    Node(id=14, section_id=5, name="dictionary"),
	    Node(id=15, section_id=6, name="import_module"),
	    Node(id=16, section_id=6, name="build_module"),
	    Node(id=17, section_id=7, name="class_intro")
	]

	node_links = [
		NodeLink(section_id=1, source=1, target=2),
		NodeLink(section_id=2, source=3, target=4),
		NodeLink(section_id=4, source=6, target=7),
		NodeLink(section_id=4, source=6, target=8),
		NodeLink(section_id=5, source=9, target=12),
		NodeLink(section_id=5, source=10, target=12),
		NodeLink(section_id=5, source=11, target=12),
		NodeLink(section_id=5, source=12, target=13),
		NodeLink(section_id=5, source=12, target=14),
		NodeLink(section_id=6, source=15, target=16)
	]

	user_domains = [
		UserDomain(user_id=1, domain_id=1, pretest=False),
		UserDomain(user_id=1, domain_id=2, pretest=False)
	]

	user_nodes = [UserNode(user_id=1, node_id=node_id, mastered=True) for node_id in range(7)] \
			   + [UserNode(user_id=1, node_id=node_id, mastered=False) for node_id in range(7, 18)]

	reads = [
		Read(id=1, node_id=7, contributor_id=0),
		Read(id=2, node_id=7, contributor_id=0),
	]

	tests = [
		Test(id=1, node_id=7, contributor_id=0),
		Test(id=2, node_id=7, contributor_id=0),
	]

	records_list = [users, domains, sections, nodes, section_links, node_links, user_domains, user_nodes, reads, tests]
	for records in records_list:
		db.session.bulk_save_objects(records)

	db.session.commit()
