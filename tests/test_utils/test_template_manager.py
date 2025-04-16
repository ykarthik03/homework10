import pytest
from unittest.mock import patch, MagicMock
from app.utils.template_manager import TemplateManager

@pytest.fixture
def template_manager():
    return TemplateManager()

def test_read_template_file_not_found(template_manager):
    with patch('builtins.open', side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            template_manager._read_template('nonexistent.md')

def test_apply_email_styles_runs(template_manager):
    # Should run even with empty HTML
    html = ''
    result = template_manager._apply_email_styles(html)
    assert isinstance(result, str)

def test_render_template_success(template_manager):
    with patch.object(template_manager, '_read_template', side_effect=["header", "footer", "main {name}"]):
        with patch('app.utils.template_manager.markdown2.markdown', return_value='<html>content</html>'):
            result = template_manager.render_template('main', name='Test')
            assert 'content' in result
