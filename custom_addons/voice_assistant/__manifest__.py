{
    'name': 'OpenAI Voice Assistant',
    'version': '1.0.0',
    'category': 'Tools',
    'summary': 'AI Voice Assistant powered by OpenAI Whisper and GPT',
    'description': '''
        Integrate OpenAI's Whisper (speech-to-text) and GPT for voice-based CRM operations.
        Features:
        - Transcribe voice messages to text
        - AI-powered CRM insights
        - Voice commands for lead management
    ''',
    'author': 'Scholarix',
    'depends': ['base', 'crm', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/voice_assistant_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'external_dependencies': {
        'python': ['openai', 'python-dotenv'],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
