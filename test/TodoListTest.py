""" Tests for the TodoList class. """

import datetime
import re
import unittest

import TodoFile
import TodoList

class TodoListTester(unittest.TestCase):
    def setUp(self):
        self.todofile = TodoFile.TodoFile('TodoListTest.txt')
        lines = [line for line in self.todofile.read() \
                       if re.search(r'\S', line)]
        self.text = ''.join(lines)
        self.todolist = TodoList.TodoList(lines)

    def test_contexts(self):
        self.assertEquals(set(['Context1', 'Context2']), \
            self.todolist.contexts())

    def test_projects(self):
        self.assertEquals(set(['Project1', 'Project2']), \
            self.todolist.projects())

    def test_add1(self):
        text = "(C) Adding a new task @Context3 +Project3"
        count = self.todolist.count()
        self.todolist.add(text)

        self.assertEquals(self.todolist.todo(count+1).source(), text)
        self.assertEquals(set(['Project1', 'Project2', 'Project3']), \
            self.todolist.projects())
        self.assertEquals(set(['Context1', 'Context2', 'Context3']), \
            self.todolist.contexts())

    def test_add2(self):
        text = str(self.todolist)
        self.todolist.add('')
        self.assertEquals(str(self.todolist), text)

    def test_add3a(self):
        count = self.todolist.count()
        self.todolist.add('\n(C) New task')

        self.assertEqual(self.todolist.count(), count + 1)
        self.assertEqual(self.todolist.todo(count + 1).source(), '(C) New task')
        self.assertEqual(self.todolist.todo(count + 1).priority(), 'C')

    def test_add3b(self):
        count = self.todolist.count()
        self.todolist.add('(C) New task\n')

        self.assertEqual(self.todolist.count(), count + 1)
        self.assertEqual(self.todolist.todo(count + 1).source(), '(C) New task')
        self.assertEqual(self.todolist.todo(count + 1).priority(), 'C')

    def test_add4(self):
        text = str(self.todolist)
        self.todolist.add(' ')
        self.assertEquals(str(self.todolist), text)

    def test_add5(self):
        text = str(self.todolist)
        self.todolist.add("\n")
        self.assertEquals(str(self.todolist), text)

    def test_delete1(self):
        count = self.todolist.count()
        self.todolist.delete(2)

        self.assertEquals(self.todolist.todo(2).source(), \
            "(C) Baz @Context1 +Project1 key:value")
        self.assertEquals(self.todolist.count(), count - 1)

    def test_delete2(self):
        count = self.todolist.count()
        self.todolist.delete(count + 1)

        self.assertEquals(self.todolist.count(), count)

    def test_append1(self):
        self.todolist.append(3, "@Context3")

        self.assertEquals(self.todolist.todo(3).source(), \
            "(C) Baz @Context1 +Project1 key:value @Context3")
        self.assertEquals(set(['Context1', 'Context2', 'Context3']), \
            self.todolist.contexts())

    def test_append2(self):
        text = self.todolist.todo(3).text()
        self.todolist.append(3, "foo:bar")

        self.assertEquals(self.todolist.todo(3).text(), text)
        self.assertEquals(self.todolist.todo(3).source(), \
            "(C) Baz @Context1 +Project1 key:value foo:bar")

    def test_append3(self):
        text = self.todolist.todo(3).text()
        self.todolist.append(3, '')

        self.assertEquals(self.todolist.todo(3).text(), text)

    def test_todo(self):
        count = self.todolist.count()
        todo = self.todolist.todo(count+100)

        self.assertEquals(todo, None)

    def test_string(self):
        # readlines() always ends a string with \n, but join() in str(todolist)
        # doesn't necessarily.
        self.assertEquals(str(self.todolist) + '\n', self.text)

    def test_count(self):
        """ Test that empty lines are not counted. """
        self.assertEquals(self.todolist.count(), 5)
