import filecmp
import os
from unittest import TestCase

import numpy as np
from OCC.Core.TopoDS import TopoDS_Shape

from pygem.cad import FFD
from pygem.cad import CADDeformation

class TestFFDCAD(TestCase):

    def test_ffd_iges_pipe_mod_through_files(self):
        ffd = FFD(None,30,30,30,1e-4)
        ffd.read_parameters(
            filename='tests/test_datasets/parameters_test_ffd_iges.prm')
        ffd('tests/test_datasets/test_pipe.iges', 'test_pipe_result.iges')
        with open('test_pipe_result.iges', "r") as created, \
             open('tests/test_datasets/test_pipe_out_true.iges', "r") as reference:
             ref = reference.readlines()[5:]
             cre = created.readlines()[5:]
             self.assertEqual(len(ref),len(cre))
             for i in range(len(cre)):
                 self.assertMultiLineEqual(ref[i], cre[i])
        self.addCleanup(os.remove, 'test_pipe_result.iges')

    def test_ffd_iges_pipe_mod_through_topods_shape(self):
        filename = 'tests/test_datasets/test_pipe_hollow.iges'
        orig_shape = CADDeformation.read_shape(filename)
        ffd = FFD(None,30,30,30,1e-4)
        ffd.read_parameters(
            filename='tests/test_datasets/parameters_test_ffd_iges.prm')
        mod_shape = ffd(orig_shape)
        CADDeformation.write_shape('test_pipe_hollow_result.iges', mod_shape)
        with open('test_pipe_hollow_result.iges', "r") as created, \
             open('tests/test_datasets/test_pipe_hollow_out_true.iges', "r") as reference:
             ref = reference.readlines()[5:]
             cre = created.readlines()[5:]
             self.assertEqual(len(ref),len(cre))
             for i in range(len(cre)):
                 self.assertMultiLineEqual(ref[i], cre[i])
        self.addCleanup(os.remove, 'test_pipe_hollow_result.iges')
