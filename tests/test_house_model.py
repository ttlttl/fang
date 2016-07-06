# -*- coding=UTF-8 -*-
import unittest
from app import create_app, db
from app.models import District, Area, Community, House

class HouseModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_district(self):
        district = District(name="hello")
        db.session.add(district)
        db.session.commit()

    def test_add_aera_setter(self):
        district_name = "test_district"
        area_name = "testarea"
        district = District(name=district_name)
        db.session.add(district)
        db.session.commit()
        d = District.query.filter_by(name=district_name).first()
        area = Area(name=area_name, district=d)
        db.session.add(area)
        db.session.commit()
        dd = District.query.filter_by(name=district_name).first()
        self.assertTrue(dd.areas.first().name == area_name)

    def test_add_community(self):
        area_name = "area_for_test"
        community_name = "test_community"
        area = Area(name=area_name)
        db.session.add(area)
        db.session.commit()
        community = Community(name=community_name, area=area)
        db.session.add(community)
        db.session.commit()
        aarea = Area().query.filter_by(name=area_name).first()
        self.assertTrue(aarea.communities.first().name == community_name)

    def test_relationships(self):
        house_title1 = "title_house1"
        house_title2 = "title_house1"
        district1 = "test_relation_district1"
        district2 = "test_relation_district2"
        area1 = "test_relation_area1"
        area2 = "test_relation_area2"
        community1 = "test_relation_c1"
        community2 = "test_relation_c2"
        d1 = District(name=district1)
        d2 = District(name=district2)
        db.session.add(d1)
        db.session.add(d2)
        db.session.commit()
        a1 = Area(name=area1, district=d1)
        a2 = Area(name=area2, district=d2)
        db.session.add(a1)
        db.session.add(a2)
        db.session.commit()
        c1 = Community(name=community1, area=a1)
        c2 = Community(name=community2, area=a2)
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()
        h1 = House(title=house_title1, community=c1)
        h2 = House(title=house_title2, community=c2)
        db.session.add(h1)
        db.session.add(h2)
        db.session.commit()
        self.assertTrue(District.query.filter_by(name=district1).first().areas.first()\
                        .communities.first().houses.first().title==house_title1)
        self.assertTrue(District.query.filter_by(name=district2).first().areas.first() \
                        .communities.first().houses.first().title == house_title2)