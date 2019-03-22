import imp

import mock


class TestActions():
    def test_example_action(self, infranode, monkeypatch):
        mock_function = mock.Mock()
        monkeypatch.setattr(infranode, 'action_function', mock_function)
        assert mock_function.call_count == 0
        imp.load_source('action_function', './actions/example-action')
        assert mock_function.call_count == 1
