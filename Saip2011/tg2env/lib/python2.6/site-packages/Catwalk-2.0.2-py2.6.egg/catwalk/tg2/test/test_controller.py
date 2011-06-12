import os, sys
#from catwalk.test.base import setup_database, setup_records
import catwalk
from tg.test_stack import TestConfig, app_from_config
from tg.util import Bunch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catwalk.tg2.test.model import metadata, DBSession

root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, root)
test_db_path = 'sqlite:///'+root+'/test.db'
paths=Bunch(
            root=root,
            controllers=os.path.join(root, 'controllers'),
            static_files=os.path.join(root, 'public'),
            templates=os.path.join(root, 'templates')
            )

base_config = TestConfig(folder = 'rendering',
                         values = {'use_sqlalchemy': True,
                                   'model':catwalk.tg2.test.model,
                                   'session':catwalk.tg2.test.model.DBSession,
                                   'pylons.helpers': Bunch(),
                                   'use_legacy_renderer': False,
                                   # this is specific to mako
                                   # to make sure inheritance works
                                   'use_dotted_templatenames': True,
                                   'paths':paths,
                                   'package':catwalk.tg2.test,
                                   'sqlalchemy.url':test_db_path
                                  }
                         )

def setup():
    engine = create_engine(test_db_path)
    metadata.bind = engine
    metadata.drop_all()
    metadata.create_all()
    session = sessionmaker(bind=engine)()
    setup_records(session)
    session.commit()

def teardown():
    os.remove(test_db_path[10:])

class TestCatwalkController:
    def __init__(self, *args, **kargs):
        self.app = app_from_config(base_config)

    def test_index(self):
        resp = self.app.get('/catwalk').follow()
        assert 'Document' in resp, resp

    def test_list_documents(self):
        resp = self.app.get('/catwalk/Document').follow()
        assert """</thead>
    <tbody>
    </tbody>
</table>
      No Records Found.
</div>
      </div>
""" in resp, resp

    def test_documents_new(self):
        resp = self.app.get('/catwalk/Document/new')
        assert """<tr id="blob.container" class="even" title="">
            <td class="labelcol">
                <label id="blob.label" for="blob" class="fieldlabel">Blob</label>
            </td>
            <td class="fieldcol">
                <input type="file" name="blob" class="filefield" id="blob" value="" />
            </td>
        </tr>""" in resp, resp
    def test_documents_metadata(self):
        resp = self.app.get('/catwalk/Document/metadata')
        assert """<td>
        String(length=500, convert_unicode=False, assert_unicode=None)
    </td>
</tr>
<tr class="even">
    <td>
        address
    </td>
    <td>
        relation
    </td>
""" in resp, resp

    def test_get_users(self):
        resp = self.app.get('/catwalk/User/')
        assert """<td>
            <a href="./1/edit">edit</a> |
            <a href="./1/delete">delete</a>
            </td>
            <td>******</td><td>1</td><td>someone</td><td>asdf@asdf.com</td>""" in resp, resp

    def test_get_users_json(self):
        resp = self.app.get('/catwalk/User.json')
        assert """{}""" in resp, resp

    def test_edit_user(self):
        resp = self.app.get('/catwalk/User/1/edit')
        assert """<td class="fieldcol">
                <select name="town" class="propertysingleselectfield" id="town">
        <option value="1" selected="selected">Arvada</option><option value="2">Denver</option><option value="3">Golden</option><option value="4">Boulder</option><option value="">-----------</option>
</select>
            </td>
        </tr><tr id="password.container" class="even" title="">
            <td class="labelcol">
                <label id="password.label" for="password" class="fieldlabel">Password</label>
            </td>
            <td class="fieldcol">
                <input type="password" name="password" class="passwordfield" id="password" value="" />
            </td>""" in resp, resp

    def test_edit_user_success(self):
        resp = self.app.post('/catwalk/User/1/', params={'sprox_id':'put__User',
                                                         '_method':'PUT',
                                                                   'user_name':'someone',
                                                                   'display_name':'someone2',
                                                                   'email_address':'asdf2@asdf2.com',
                                                                   '_password':'pass',
                                                                   'password':'pass',
                                                                   'town':'1',
                                                                   'town_id':'1',
                                                                   'user_id':'1',
                                                                   'created':'2009-01-11 13:54:01'}).follow()
        assert '<td>******</td><td>1</td><td>someone</td><td>asdf2@asdf2.com</td>' in resp, resp
        resp = self.app.post('/catwalk/User/1/', params={'sprox_id':'put__User',
                                                         '_method':'PUT',
                                                                   'user_name':'someone',
                                                                   'display_name':'someone2',
                                                                   'email_address':'asdf@asdf.com',
                                                                   '_password':'pass',
                                                                   'password':'pass',
                                                                   'town':'1',
                                                                   'town_id':'1',
                                                                   'user_id':'1',
                                                                   'created':'2009-01-11 13:54:01'}).follow()
        assert '<td>******</td><td>1</td><td>someone</td><td>asdf@asdf.com</td>' in resp, resp

    def test_add_and_remove_user(self):
        resp = self.app.post('/catwalk/User/', params={'sprox_id':'add__User',
                                                                   'user_name':'someone',
                                                                   'display_name':'someone2',
                                                                   'email_address':'asdf2@asdf2.com',
                                                                   '_password':'pass',
                                                                   'password':'pass',
                                                                   'town':'1',
                                                                   'town_id':'1',
                                                                   'user_id':'2',
                                                                   'created':'2009-01-11 13:54:01'}).follow()
        assert '<td>asdf2@asdf2' in resp, resp
        resp = self.app.get('/catwalk/User/2/', params={'user_id':'2', '_method':'DELETE'}).follow()
        assert 'asdf2@asdf2' not in resp, resp

    def test_add_user_existing_username(self):
        resp = self.app.post('/catwalk/User/create', params={'sprox_id':'add__User',
                                                                   'user_name':u'asdf',
                                                                   'display_name':'someone2',
                                                                   'email_address':'asdf2@asdf2.com',
                                                                   '_password':'pass',
                                                                   'password':'pass',
                                                                   'town':'1',
                                                                   'town_id':'1',
                                                                   'user_id':'2',
                                                                   'created':'2009-01-11 13:54:01'})
        assert 'That value already exists' in resp, resp
