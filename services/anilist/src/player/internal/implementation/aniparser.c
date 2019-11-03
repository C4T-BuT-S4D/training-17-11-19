#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include "structmember.h"

const Py_ssize_t MAX_LEN = 10000;

typedef struct {
    PyObject_HEAD
    char* data;
    char* fname;
    Py_ssize_t length;
} Aniparser;

static PyModuleDef aniparser = {
    PyModuleDef_HEAD_INIT,
    .m_name = "custom",
    .m_doc = "Aniparser module",
    .m_size = -1,
};

static int
Aniparser_init(Aniparser *self, PyObject *args) {
    char *s1;
    char *s2;

    Py_ssize_t len1;
    Py_ssize_t len2;

    if (!PyArg_ParseTuple(args, "s#s#", &s1, &len1, &s2, &len2))
    {
        return -1;
    }

    self->data = malloc(len1 - 7);
    self->fname = malloc(len2 + 1);

    memcpy(self->data, s1 + 8, len1 - 8);
    self->data[len1 - 8] = 0;

    memcpy(self->fname, s2, len2);
    self->fname[len2] = 0;

    self->length = *((size_t*)s1);
    if (self->length > MAX_LEN) {
        self->length = MAX_LEN;
    }

    return 0;
}

static PyMemberDef Aniparser_members[] = {
    {"data", T_STRING, offsetof(Aniparser, data), 0, "string with data to parse"},
    {"fname", T_STRING, offsetof(Aniparser, fname), 0, "filename"},
    {"length", T_PYSSIZET, offsetof(Aniparser, length), 0, "data length"},
    {NULL}  /* Sentinel */
};

static PyObject *
Aniparser_parse(Aniparser *self) {
    char *buf = alloca(strlen(self->data));
    memcpy(buf, self->data, self->length);

    PyObject *result = Py_BuildValue("y#", buf, self->length);
    return result;
}

static PyObject *
Aniparser_create(Aniparser *self) {
    char *buf = alloca(strlen(self->data));
    memcpy(buf, self->data, strlen(self->data));
    FILE* fp = fopen(self->fname, "w");
    if (!fp) {
        Py_RETURN_NONE;
    }
    fwrite((char*)(&(self->length)), 1, sizeof(Py_ssize_t), fp);
    fwrite(buf, 1, self->length, fp);
    fclose(fp);

    Py_RETURN_NONE;
}

static PyMethodDef Aniparser_methods[] = {
    {"parse", (PyCFunction) Aniparser_parse, METH_NOARGS, "Parse data"},
    {"create", (PyCFunction) Aniparser_create, METH_NOARGS, "Create data frame"},
    {NULL}  /* Sentinel */
};

static PyTypeObject AniparserType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "aniparser.Aniparser",
    .tp_doc = "Aniparser object",
    .tp_basicsize = sizeof(Aniparser),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc) Aniparser_init,
    .tp_members = Aniparser_members,
    .tp_methods = Aniparser_methods,
};

PyMODINIT_FUNC
PyInit_aniparser(void)
{
    PyObject *m;
    if (PyType_Ready(&AniparserType) < 0)
        return NULL;

    m = PyModule_Create(&aniparser);
    if (m == NULL)
        return NULL;

    Py_INCREF(&AniparserType);
    PyModule_AddObject(m, "Aniparser", (PyObject *) &AniparserType);
    return m;
}
