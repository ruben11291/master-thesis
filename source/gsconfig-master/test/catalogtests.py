import re
import unittest
from geoserver.catalog import Catalog, ConflictingDataError, UploadError, \
    FailedRequestError
from geoserver.support import ResourceInfo, url
from geoserver.layergroup import LayerGroup
from geoserver.util import shapefile_and_friends

class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.cat = Catalog("http://localhost:8080/geoserver/rest")

    def testAbout(self):
        about_html = self.cat.about()
        self.assertTrue('<html xmlns="http://www.w3.org/1999/xhtml"' in about_html)

    def testGSVersion(self):
        version = self.cat.gsversion()
        pat = re.compile('\d\.\d(\.[\dx]|-SNAPSHOT)')
        self.assertTrue(pat.match('2.2.x'))
        self.assertTrue(pat.match('2.3.2'))
        self.assertTrue(pat.match('2.3-SNAPSHOT'))
        self.assertFalse(pat.match('2.3.y'))
        self.assertFalse(pat.match('233'))
        self.assertTrue(pat.match(version))

    def testWorkspaces(self):
        self.assertEqual(7, len(self.cat.get_workspaces()))
        # marking out test since geoserver default workspace is not consistent 
        # self.assertEqual("cite", self.cat.get_default_workspace().name)
        self.assertEqual("topp", self.cat.get_workspace("topp").name)


    def testStores(self):
        topp = self.cat.get_workspace("topp")
        sf = self.cat.get_workspace("sf")
        self.assertEqual(9, len(self.cat.get_stores()))
        self.assertEqual(2, len(self.cat.get_stores(topp)))
        self.assertEqual(2, len(self.cat.get_stores(sf)))
        self.assertEqual("states_shapefile", self.cat.get_store("states_shapefile", topp).name)
        self.assertEqual("states_shapefile", self.cat.get_store("states_shapefile").name)
        self.assertEqual("states_shapefile", self.cat.get_store("states_shapefile").name)
        self.assertEqual("sfdem", self.cat.get_store("sfdem", sf).name)
        self.assertEqual("sfdem", self.cat.get_store("sfdem").name)

  
    def testResources(self):
        topp = self.cat.get_workspace("topp")
        sf = self.cat.get_workspace("sf")
        states = self.cat.get_store("states_shapefile", topp)
        sfdem = self.cat.get_store("sfdem", sf)
        self.assertEqual(19, len(self.cat.get_resources()))
        self.assertEqual(1, len(self.cat.get_resources(states)))
        self.assertEqual(5, len(self.cat.get_resources(workspace=topp)))
        self.assertEqual(1, len(self.cat.get_resources(sfdem)))
        self.assertEqual(6, len(self.cat.get_resources(workspace=sf)))

        self.assertEqual("states", self.cat.get_resource("states", states).name)
        self.assertEqual("states", self.cat.get_resource("states", workspace=topp).name)
        self.assertEqual("states", self.cat.get_resource("states").name)
        states = self.cat.get_resource("states")

        fields = [
            states.title,
            states.abstract,
            states.native_bbox,
            states.latlon_bbox,
            states.projection,
            states.projection_policy
        ]

        self.assertFalse(None in fields, str(fields))
        self.assertFalse(len(states.keywords) == 0)
        self.assertFalse(len(states.attributes) == 0)
        self.assertTrue(states.enabled)

        self.assertEqual("sfdem", self.cat.get_resource("sfdem", sfdem).name)
        self.assertEqual("sfdem", self.cat.get_resource("sfdem", workspace=sf).name)
        self.assertEqual("sfdem", self.cat.get_resource("sfdem").name)


    def testLayers(self):
        expected = set(["Arc_Sample", "Pk50095", "Img_Sample", "mosaic", "sfdem",
            "bugsites", "restricted", "streams", "archsites", "roads",
            "tasmania_roads", "tasmania_water_bodies", "tasmania_state_boundaries",
            "tasmania_cities", "states", "poly_landmarks", "tiger_roads", "poi",
            "giant_polygon"
        ])
        actual = set(l.name for l in self.cat.get_layers())
        missing = expected - actual
        extras = actual - expected
        message = "Actual layer list did not match expected! (Extras: %s) (Missing: %s)" % (extras, missing)
        self.assert_(len(expected ^ actual) == 0, message)

        states = self.cat.get_layer("states")

        self.assert_("states", states.name)
        self.assert_(isinstance(states.resource, ResourceInfo))
        self.assertEqual(set(s.name for s in states.styles), set(['pophatch', 'polygon']))
        self.assertEqual(states.default_style.name, "population")

    def testLayerGroups(self):
        expected = set(["tasmania", "tiger-ny", "spearfish"])
        actual = set(l.name for l in self.cat.get_layergroups())
        missing = expected - actual
        extras = actual - expected
        message = "Actual layergroup list did not match expected! (Extras: %s) (Missing: %s)" % (extras, missing)
        self.assert_(len(expected ^ actual) == 0, message)

        tas = self.cat.get_layergroup("tasmania")

        self.assert_("tasmania", tas.name)
        self.assert_(isinstance(tas, LayerGroup))
        self.assertEqual(tas.layers, ['tasmania_state_boundaries', 'tasmania_water_bodies', 'tasmania_roads', 'tasmania_cities'], tas.layers)
        self.assertEqual(tas.styles, [None, None, None, None], tas.styles)

    def testStyles(self):
        self.assertEqual(20, len(self.cat.get_styles()))
        self.assertEqual("population", self.cat.get_style("population").name)
        self.assertEqual("popshade.sld", self.cat.get_style("population").filename)
        self.assertEqual("population", self.cat.get_style("population").sld_name)
        self.assert_(self.cat.get_style('non-existing-style') is None)

    def testEscaping(self):
        # GSConfig is inconsistent about using exceptions vs. returning None
        # when a resource isn't found.
        # But the basic idea is that none of them should throw HTTP errors from
        # misconstructed URLS
        self.cat.get_style("best style ever")
        self.cat.get_workspace("best workspace ever")
        try:
            self.cat.get_store(workspace="best workspace ever",
                name="best store ever")
            self.fail('expected exception')
        except FailedRequestError, fre:
            self.assertEqual('No store found named: best store ever', fre.message)
        try:
            self.cat.get_resource(workspace="best workspace ever",
                store="best store ever",
                name="best resource ever")
        except FailedRequestError, fre:
            self.assertEqual('No store found named: best store ever', fre.message)
        self.cat.get_layer("best layer ever")
        self.cat.get_layergroup("best layergroup ever")

    def testUnicodeUrl(self):
        """
        Tests that the geoserver.support.url function support unicode strings.
        """

        # Test the url function with unicode
        seg = ['workspaces', 'test', 'datastores', u'operaci\xf3n_repo', 'featuretypes.xml']
        u = url(base=self.cat.service_url, seg=seg)
        self.assertEqual(u, self.cat.service_url + "/workspaces/test/datastores/operaci%C3%B3n_repo/featuretypes.xml")

        # Test the url function with normal string
        seg = ['workspaces', 'test', 'datastores', 'test-repo', 'featuretypes.xml']
        u = url(base=self.cat.service_url, seg=seg)
        self.assertEqual(u, self.cat.service_url + "/workspaces/test/datastores/test-repo/featuretypes.xml")


class ModifyingTests(unittest.TestCase):
    def setUp(self):
        self.cat = Catalog("http://localhost:8080/geoserver/rest")

    def testFeatureTypeSave(self):
        # test saving round trip
        rs = self.cat.get_resource("bugsites")
        old_abstract = rs.abstract
        new_abstract = "Not the original abstract"
        enabled = rs.enabled

        # Change abstract on server
        rs.abstract = new_abstract
        self.cat.save(rs)
        rs = self.cat.get_resource("bugsites")
        self.assertEqual(new_abstract, rs.abstract)
        self.assertEqual(enabled, rs.enabled)

        # Change keywords on server
        rs.keywords = ["bugsites", "gsconfig"]
        enabled = rs.enabled
        self.cat.save(rs)
        rs = self.cat.get_resource("bugsites")
        self.assertEqual(["bugsites", "gsconfig"], rs.keywords)
        self.assertEqual(enabled, rs.enabled)
        
        # Change metadata links on server
        rs.metadata_links = [("text/xml", "TC211", "http://example.com/gsconfig.test.metadata")]
        enabled = rs.enabled
        self.cat.save(rs)
        rs = self.cat.get_resource("bugsites")
        self.assertEqual(
                        [("text/xml", "TC211", "http://example.com/gsconfig.test.metadata")],
                        rs.metadata_links)
        self.assertEqual(enabled, rs.enabled)


        # Restore abstract
        rs.abstract = old_abstract
        self.cat.save(rs)
        rs = self.cat.get_resource("bugsites")
        self.assertEqual(old_abstract, rs.abstract)

    def testDataStoreCreate(self):
        ds = self.cat.create_datastore("vector_gsconfig")
        ds.connection_parameters.update(
            host="localhost", port="5432", database="db", user="postgres",
            passwd="password", dbtype="postgis")
        self.cat.save(ds)

    def testPublishFeatureType(self):
        # Use the other test and store creation to load vector data into a database
        # @todo maybe load directly to database?
        try:
            self.testDataStoreCreateAndThenAlsoImportData()
        except FailedRequestError:
            pass
        try:
            lyr = self.cat.get_layer('import')
            # Delete the existing layer and resource to allow republishing.
            self.cat.delete(lyr)
            self.cat.delete(lyr.resource)
            ds = self.cat.get_store("gsconfig_import_test")
            # make sure it's gone
            self.assert_(self.cat.get_layer('import') is None)
            self.cat.publish_featuretype("import", ds, native_crs="EPSG:4326")
            # and now it's not
            self.assert_(self.cat.get_layer('import') is not None)
        finally:
            # tear stuff down to allow the other test to pass if we run first
            ds = self.cat.get_store("gsconfig_import_test")
            lyr = self.cat.get_layer('import')
            # Delete the existing layer and resource to allow republishing.
            self.cat.delete(lyr)
            self.cat.delete(lyr.resource)
            self.cat.delete(ds)

    def testDataStoreModify(self):
        ds = self.cat.get_store("sf")
        self.assertFalse("foo" in ds.connection_parameters)
        ds.connection_parameters = ds.connection_parameters
        ds.connection_parameters["foo"] = "bar"
        orig_ws = ds.workspace.name
        self.cat.save(ds)
        ds = self.cat.get_store("sf")
        self.assertTrue("foo" in ds.connection_parameters)
        self.assertEqual("bar", ds.connection_parameters["foo"])
        self.assertEqual(orig_ws, ds.workspace.name)

    def testDataStoreCreateAndThenAlsoImportData(self):
        ds = self.cat.create_datastore("gsconfig_import_test")
        ds.connection_parameters.update(
            host="localhost", port="5432", database="db", user="postgres",
            passwd="password", dbtype="postgis")
        self.cat.save(ds)
        ds = self.cat.get_store("gsconfig_import_test")
        self.cat.add_data_to_store(ds, "import", {
            'shp': 'test/data/states.shp',
            'shx': 'test/data/states.shx',
            'dbf': 'test/data/states.dbf',
            'prj': 'test/data/states.prj'
        })

    def testCoverageStoreCreate(self):
        ds = self.cat.create_coveragestore2("coverage_gsconfig")
        ds.data_url = "file:data/mytiff.tiff"
        self.cat.save(ds)

    def testCoverageStoreModify(self):
        cs = self.cat.get_store("sfdem")
        self.assertEqual("GeoTIFF", cs.type)
        cs.type = "WorldImage"
        self.cat.save(cs)
        cs = self.cat.get_store("sfdem")
        self.assertEqual("WorldImage", cs.type)

        # not sure about order of test runs here, but it might cause problems
        # for other tests if this layer is misconfigured
        cs.type = "GeoTIFF"
        self.cat.save(cs) 

    def testCoverageSave(self):
        # test saving round trip
        rs = self.cat.get_resource("Arc_Sample")
        old_abstract = rs.abstract
        new_abstract = "Not the original abstract"

        # # Change abstract on server
        rs.abstract = new_abstract
        self.cat.save(rs)
        rs = self.cat.get_resource("Arc_Sample")
        self.assertEqual(new_abstract, rs.abstract)

        # Restore abstract
        rs.abstract = old_abstract
        self.cat.save(rs)
        rs = self.cat.get_resource("Arc_Sample")
        self.assertEqual(old_abstract, rs.abstract)

        # Change metadata links on server
        rs.metadata_links = [("text/xml", "TC211", "http://example.com/gsconfig.test.metadata")]
        enabled = rs.enabled
        self.cat.save(rs)
        rs = self.cat.get_resource("Arc_Sample")
        self.assertEqual(
            [("text/xml", "TC211", "http://example.com/gsconfig.test.metadata")],
            rs.metadata_links)
        self.assertEqual(enabled, rs.enabled)

        srs_before = set(['EPSG:4326'])
        srs_after = set(['EPSG:4326', 'EPSG:3785'])
        formats = set(['ARCGRID', 'ARCGRID-GZIP', 'GEOTIFF', 'PNG', 'GIF', 'TIFF'])
        formats_after = set(["PNG", "GIF", "TIFF"])

        # set and save request_srs_list
        self.assertEquals(set(rs.request_srs_list), srs_before, str(rs.request_srs_list))
        rs.request_srs_list = rs.request_srs_list + ['EPSG:3785']
        self.cat.save(rs)
        rs = self.cat.get_resource("Arc_Sample")
        self.assertEquals(set(rs.request_srs_list), srs_after, str(rs.request_srs_list))

        # set and save response_srs_list
        self.assertEquals(set(rs.response_srs_list), srs_before, str(rs.response_srs_list))
        rs.response_srs_list = rs.response_srs_list + ['EPSG:3785']
        self.cat.save(rs)
        rs = self.cat.get_resource("Arc_Sample")
        self.assertEquals(set(rs.response_srs_list), srs_after, str(rs.response_srs_list))

        # set and save supported_formats
        self.assertEquals(set(rs.supported_formats), formats, str(rs.supported_formats))
        rs.supported_formats = ["PNG", "GIF", "TIFF"]
        self.cat.save(rs)
        rs = self.cat.get_resource("Arc_Sample")
        self.assertEquals(set(rs.supported_formats), formats_after, str(rs.supported_formats))

    def testWmsStoreCreate(self):
        ws = self.cat.create_wmsstore("wmsstore_gsconfig")
        ws.capabilitiesURL = "http://suite.opengeo.org/geoserver/ows?service=wms&version=1.1.1&request=GetCapabilities"
        ws.type = "WMS"
        self.cat.save(ws)
     
    def testWmsLayer(self):
        self.cat.create_workspace("wmstest", "http://example.com/wmstest")
        wmstest = self.cat.get_workspace("wmstest")
        wmsstore = self.cat.create_wmsstore("wmsstore", wmstest)
        wmsstore.capabilitiesURL = "http://suite.opengeo.org/geoserver/ows?service=wms&version=1.1.1&request=GetCapabilities"
        wmsstore.type = "WMS"
        self.cat.save(wmsstore)
        wmsstore = self.cat.get_store("wmsstore")
        self.assertEqual(1, len(self.cat.get_stores(wmstest)))
        available_layers = wmsstore.get_resources(available=True)
        for layer in available_layers:
            new_layer = self.cat.create_wmslayer(wmstest, wmsstore, layer)
        added_layers = wmsstore.get_resources()
        self.assertEqual(len(available_layers), len(added_layers))

    def testFeatureTypeCreate(self):
        shapefile_plus_sidecars = shapefile_and_friends("test/data/states")
        expected = {
            'shp': 'test/data/states.shp',
            'shx': 'test/data/states.shx',
            'dbf': 'test/data/states.dbf',
            'prj': 'test/data/states.prj'
        }

        self.assertEqual(len(expected), len(shapefile_plus_sidecars))
        for k, v in expected.iteritems():
            self.assertEqual(v, shapefile_plus_sidecars[k])
 
        sf = self.cat.get_workspace("sf")
        self.cat.create_featurestore("states_test", shapefile_plus_sidecars, sf)

        self.assert_(self.cat.get_resource("states_test", workspace=sf) is not None)

        self.assertRaises(
            ConflictingDataError, 
            lambda: self.cat.create_featurestore("states_test", shapefile_plus_sidecars, sf)
        )

        self.assertRaises(
            UploadError,
            lambda: self.cat.create_coveragestore("states_raster_test", shapefile_plus_sidecars, sf)
        )

        bogus_shp = {
            'shp': 'test/data/Pk50095.tif',
            'shx': 'test/data/Pk50095.tif',
            'dbf':    'test/data/Pk50095.tfw',
            'prj':    'test/data/Pk50095.prj'
        }

        self.assertRaises(
            UploadError,
            lambda: self.cat.create_featurestore("bogus_shp", bogus_shp, sf)
        )

        lyr = self.cat.get_layer("states_test")
        self.cat.delete(lyr)
        self.assert_(self.cat.get_layer("states_test") is None)


    def testCoverageCreate(self):
        tiffdata = {
            'tiff': 'test/data/Pk50095.tif',
            'tfw':    'test/data/Pk50095.tfw',
            'prj':    'test/data/Pk50095.prj'
        }

        sf = self.cat.get_workspace("sf")
        # TODO: Uploading WorldImage file no longer works???
        # ft = self.cat.create_coveragestore("Pk50095", tiffdata, sf)

        # self.assert_(self.cat.get_resource("Pk50095", workspace=sf) is not None)

        # self.assertRaises(
        #         ConflictingDataError, 
        #         lambda: self.cat.create_coveragestore("Pk50095", tiffdata, sf)
        # )

        self.assertRaises(
            UploadError, 
            lambda: self.cat.create_featurestore("Pk50095_vector", tiffdata, sf)
        )

        bogus_tiff = {
            'tiff': 'test/data/states.shp',
            'tfw': 'test/data/states.shx',
            'prj': 'test/data/states.prj'
        }

        self.assertRaises(
            UploadError,
            lambda: self.cat.create_coveragestore("states_raster", bogus_tiff)
        )

    def testLayerSave(self):
        # test saving round trip
        lyr = self.cat.get_layer("states")
        old_attribution = lyr.attribution
        new_attribution = "Not the original attribution"

        # change attribution on server
        lyr.attribution = new_attribution
        self.cat.save(lyr)
        lyr = self.cat.get_layer("states")
        self.assertEqual(new_attribution, lyr.attribution)

        # Restore attribution
        lyr.attribution = old_attribution
        self.cat.save(lyr)
        lyr = self.cat.get_layer("states")
        self.assertEqual(old_attribution, lyr.attribution)

        self.assertEqual(lyr.default_style.name, "population")
     
        old_default_style = lyr.default_style
        lyr.default_style = (s for s in lyr.styles if s.name == "pophatch").next()
        lyr.styles = [old_default_style]
        self.cat.save(lyr)
        lyr = self.cat.get_layer("states")
        self.assertEqual(lyr.default_style.name, "pophatch")
        self.assertEqual([s.name for s in lyr.styles], ["population"])


    def testStyles(self):
        # upload new style, verify existence
        self.cat.create_style("fred", open("test/fred.sld").read())
        fred = self.cat.get_style("fred")
        self.assert_(fred is not None)
        self.assertEqual("Fred", fred.sld_title)

        # replace style, verify changes
        self.cat.create_style("fred", open("test/ted.sld").read(), overwrite=True)
        fred = self.cat.get_style("fred")
        self.assert_(fred is not None)
        self.assertEqual("Ted", fred.sld_title)

        # delete style, verify non-existence
        self.cat.delete(fred, purge=True)
        self.assert_(self.cat.get_style("fred") is None)

        # attempt creating new style
        self.cat.create_style("fred", open("test/fred.sld").read())
        fred = self.cat.get_style("fred")
        self.assertEqual("Fred", fred.sld_title)

        # verify it can be found via URL and check the name
        f = self.cat.get_style_by_url(fred.href)
        self.assert_(f is not None)
        self.assertEqual(f.name, fred.name)

    def testWorkspaceStyles(self):
        # upload new style, verify existence
        self.cat.create_style("jed", open("test/fred.sld").read(), workspace="topp")

        jed = self.cat.get_style("jed", workspace="blarny")
        self.assert_(jed is None)
        jed = self.cat.get_style("jed", workspace="topp")
        self.assert_(jed is not None)
        self.assertEqual("Fred", jed.sld_title)
        jed = self.cat.get_style("topp:jed")
        self.assert_(jed is not None)
        self.assertEqual("Fred", jed.sld_title)

        # replace style, verify changes
        self.cat.create_style("jed", open("test/ted.sld").read(), overwrite=True, workspace="topp")
        jed = self.cat.get_style("jed", workspace="topp")
        self.assert_(jed is not None)
        self.assertEqual("Ted", jed.sld_title)

        # delete style, verify non-existence
        self.cat.delete(jed, purge=True)
        self.assert_(self.cat.get_style("jed", workspace="topp") is None)

        # attempt creating new style
        self.cat.create_style("jed", open("test/fred.sld").read(), workspace="topp")
        jed = self.cat.get_style("jed", workspace="topp")
        self.assertEqual("Fred", jed.sld_title)

        # verify it can be found via URL and check the full name
        f = self.cat.get_style_by_url(jed.href)
        self.assert_(f is not None)
        self.assertEqual(f.fqn, jed.fqn)

    def testLayerWorkspaceStyles(self):
        # upload new style, verify existence
        self.cat.create_style("ned", open("test/fred.sld").read(), overwrite=True, workspace="topp")
        self.cat.create_style("zed", open("test/ted.sld").read(), overwrite=True, workspace="topp")
        ned = self.cat.get_style("ned", workspace="topp")
        zed = self.cat.get_style("zed", workspace="topp")
        self.assert_(ned is not None)
        self.assert_(zed is not None)

        lyr = self.cat.get_layer("states")
        lyr.default_style = ned
        lyr.styles = [zed]
        self.cat.save(lyr)
        self.assertEqual("topp:ned", lyr.default_style)
        self.assertEqual([zed], lyr.styles)

        lyr.refresh()
        self.assertEqual("topp:ned", lyr.default_style.fqn)
        self.assertEqual([zed.fqn], [s.fqn for s in lyr.styles])

    def testWorkspaceCreate(self):
        ws = self.cat.get_workspace("acme")
        self.assertEqual(None, ws)
        self.cat.create_workspace("acme", "http://example.com/acme")
        ws = self.cat.get_workspace("acme")
        self.assertEqual("acme", ws.name)

    def testWorkspaceDelete(self): 
        self.cat.create_workspace("foo", "http://example.com/foo")
        ws = self.cat.get_workspace("foo")
        self.cat.delete(ws)
        ws = self.cat.get_workspace("foo")
        self.assert_(ws is None)

    def testWorkspaceDefault(self):
        # save orig
        orig = self.cat.get_default_workspace()
        neu = self.cat.create_workspace("neu", "http://example.com/neu")
        try:
            # make sure setting it works
            self.cat.set_default_workspace("neu")
            ws = self.cat.get_default_workspace()
            self.assertEqual('neu', ws.name)
        finally:
            # cleanup and reset to the way things were
            self.cat.delete(neu)
            self.cat.set_default_workspace(orig.name)
            ws = self.cat.get_default_workspace()
            self.assertEqual(orig.name, ws.name)

    def testFeatureTypeDelete(self):
        pass

    def testCoverageDelete(self):
        pass

    def testDataStoreDelete(self):
        states = self.cat.get_store('states_shapefile')
        self.assert_(states.enabled == True)
        states.enabled = False
        self.assert_(states.enabled == False)
        self.cat.save(states)

        states = self.cat.get_store('states_shapefile')
        self.assert_(states.enabled == False)

        states.enabled = True
        self.cat.save(states)

        states = self.cat.get_store('states_shapefile')
        self.assert_(states.enabled == True)

    def testLayerGroupSave(self):
        tas = self.cat.get_layergroup("tasmania")

        self.assertEqual(tas.layers, ['tasmania_state_boundaries', 'tasmania_water_bodies', 'tasmania_roads', 'tasmania_cities'], tas.layers)
        self.assertEqual(tas.styles, [None, None, None, None], tas.styles)

        tas.layers = tas.layers[:-1]
        tas.styles = tas.styles[:-1]

        self.cat.save(tas)

        # this verifies the local state
        self.assertEqual(tas.layers, ['tasmania_state_boundaries', 'tasmania_water_bodies', 'tasmania_roads'], tas.layers)
        self.assertEqual(tas.styles, [None, None, None], tas.styles)

        # force a refresh to check the remote state
        tas.refresh()
        self.assertEqual(tas.layers, ['tasmania_state_boundaries', 'tasmania_water_bodies', 'tasmania_roads'], tas.layers)
        self.assertEqual(tas.styles, [None, None, None], tas.styles)

if __name__ == "__main__":
    unittest.main()
