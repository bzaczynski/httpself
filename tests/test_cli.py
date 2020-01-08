from unittest import mock

import pytest
from httpself.cli import parse_args, main


class TestArgumentParser:

    def test_default_values(self):
        args = parse_args([])
        assert args.port == 443
        assert args.public is False

    def test_custom_port_number(self):
        args = parse_args(['--port', '8443'])
        assert args.port == 8443
        assert args.public is False

    def test_custom_port_number_short(self):
        args = parse_args(['-p', '8443'])
        assert args.port == 8443
        assert args.public is False

    def test_custom_port_number_float(self):
        with pytest.raises(SystemExit):
            parse_args(['--port', '3.14'])

    def test_custom_port_number_str(self):
        with pytest.raises(SystemExit):
            parse_args(['--port', 'text'])

    def test_public(self):
        args = parse_args(['--public'])
        assert args.port == 443
        assert args.public is True

    def test_public_custom_port_number(self):
        args = parse_args(['--public', '--port', '8443'])
        assert args.port == 8443
        assert args.public is True

    def test_public_custom_port_number_short(self):
        args = parse_args(['--public', '-p', '8443'])
        assert args.port == 8443
        assert args.public is True

    def test_custom_port_number_public(self):
        args = parse_args(['--port', '8443', '--public'])
        assert args.port == 8443
        assert args.public is True

    def test_custom_port_number_short_public(self):
        args = parse_args(['-p', '8443', '--public'])
        assert args.port == 8443
        assert args.public is True


@mock.patch('https_server.cli.get_self_signed_certificate')
@mock.patch('https_server.cli.run_server')
@mock.patch('os.remove')
class TestHostname:

    def test_should_run_on_localhost(self, mock_remove, mock_run, mock_get_self_signed_certificate):

        # given
        mock_get_self_signed_certificate.return_value = '/tmp/tmpwyd892qj'
        mock_args = mock.Mock(public=False, port=443)

        # when
        main(mock_args)

        # then
        mock_get_self_signed_certificate.assert_called_once_with('localhost')
        mock_run.assert_called_once_with(('localhost', 443), '/tmp/tmpwyd892qj')
        mock_remove.assert_called_once_with('/tmp/tmpwyd892qj')

    def test_should_run_on_all_interfaces(self, mock_remove, mock_run, mock_get_self_signed_certificate):

        # given
        mock_get_self_signed_certificate.return_value = '/tmp/tmpwyd892qj'
        mock_args = mock.Mock(public=True, port=443)

        # when
        main(mock_args)

        # then
        mock_get_self_signed_certificate.assert_called_once_with('0.0.0.0')
        mock_run.assert_called_once_with(('0.0.0.0', 443), '/tmp/tmpwyd892qj')
        mock_remove.assert_called_once_with('/tmp/tmpwyd892qj')
