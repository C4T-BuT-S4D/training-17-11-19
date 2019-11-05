#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include "structmember.h"

const Py_ssize_t MAX_LEN = 10000;
const Py_ssize_t MAX_DEN = 255;

Py_ssize_t load(char *src, Py_ssize_t src_len, char* dst) {
    Py_ssize_t dst_len = 0;
    dst = malloc(MAX_DEN * src_len);
    for (int i = 0; i < src_len; i += 2) {
        for (char j = 0; j < src[i]; ++j) {
            dst[dst_len++] = src[i + 1];
        }
    }
    return dst_len;
}

void dump(char *data, Py_ssize_t length, FILE *fp) {
    char *result = alloca(2 * length);

    Py_ssize_t cnt = 0;
    char cur_length = 0;
    char cur_char = 0;

    for (int i = 0; i < length; ++i) {
        if (cur_length && data[i] == cur_char) {
           ++cur_length;
        } else if (!cur_length) {
           cur_length = 1;
           cur_char = data[i];
        } else {
           result[cnt++] = cur_length;
           result[cnt++] = cur_char;
           cur_length = 1;
           cur_char = data[i];
        }

        if (cur_length == MAX_DEN) {
           result[cnt++] = cur_length;
           result[cnt++] = cur_char;
           cur_length = 0;
        }
    }
    if (cur_length) {
        result[cnt++] = cur_length;
        result[cnt++] = cur_char;
    }

    fwrite((char*)(&(cnt)), 1, sizeof(Py_ssize_t), fp);
    fwrite(result, 1, cnt, fp);
}

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

    char* res = 0;
    Py_ssize_t res_len = load(buf, self->length, res);

    PyObject *result = Py_BuildValue("y#", res, res_len);
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

    dump(buf, self->length, fp);
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
