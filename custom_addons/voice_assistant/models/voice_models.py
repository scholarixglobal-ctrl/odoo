# OpenAI Voice Assistant Models
from odoo import models, fields, api
from odoo.exceptions import UserError
import openai
import base64
import io

class VoiceAssistantSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    openai_api_key = fields.Char(
        'OpenAI API Key',
        config_parameter='voice_assistant.openai_api_key',
        groups='base.group_system',
        help='Your OpenAI API key for Whisper and GPT models'
    )
    openai_model = fields.Selection(
        [
            ('gpt-4', 'GPT-4 (Most capable)'),
            ('gpt-4-turbo', 'GPT-4 Turbo'),
            ('gpt-3.5-turbo', 'GPT-3.5 Turbo (Fast & economical)'),
        ],
        'OpenAI Model',
        config_parameter='voice_assistant.openai_model',
        default='gpt-3.5-turbo',
        help='Select the GPT model for AI responses'
    )


class VoiceMessage(models.Model):
    _name = 'voice.message'
    _description = 'Voice Message'
    _rec_name = 'transcription'
    
    name = fields.Char('Title', required=True)
    audio_file = fields.Binary('Audio File', required=True)
    filename = fields.Char('Filename')
    transcription = fields.Text('Transcription', readonly=True)
    ai_response = fields.Text('AI Response')
    duration = fields.Float('Duration (seconds)')
    create_date = fields.Datetime('Created', readonly=True)
    user_id = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user)
    lead_id = fields.Many2one('crm.lead', 'Related Lead', ondelete='set null')
    
    @api.model
    def transcribe_audio(self, audio_data, filename='audio.wav'):
        """Transcribe audio using OpenAI Whisper"""
        api_key = self.env['ir.config_parameter'].sudo().get_param('voice_assistant.openai_api_key')
        
        if not api_key:
            raise UserError('OpenAI API Key not configured. Please set it in Settings.')
        
        try:
            openai.api_key = api_key
            
            # Decode audio data
            audio_bytes = base64.b64decode(audio_data)
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = filename
            
            # Call Whisper API
            transcript = openai.Audio.transcribe(
                model='whisper-1',
                file=audio_file,
            )
            
            return transcript['text']
        except Exception as e:
            raise UserError(f'Transcription failed: {str(e)}')
    
    @api.model
    def get_ai_response(self, prompt):
        """Get response from GPT using provided prompt"""
        api_key = self.env['ir.config_parameter'].sudo().get_param('voice_assistant.openai_api_key')
        model = self.env['ir.config_parameter'].sudo().get_param('voice_assistant.openai_model', 'gpt-3.5-turbo')
        
        if not api_key:
            raise UserError('OpenAI API Key not configured. Please set it in Settings.')
        
        try:
            openai.api_key = api_key
            
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {'role': 'system', 'content': 'You are a helpful CRM assistant for Odoo. Help users manage leads, opportunities, and customer relationships.'},
                    {'role': 'user', 'content': prompt}
                ],
                temperature=0.7,
                max_tokens=500,
            )
            
            return response['choices'][0]['message']['content']
        except Exception as e:
            raise UserError(f'AI Response failed: {str(e)}')
    
    def button_transcribe(self):
        """Transcribe the audio file"""
        self.transcription = self.transcribe_audio(self.audio_file, self.filename)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Audio transcribed successfully',
                'type': 'success',
                'sticky': False,
            }
        }
    
    def button_get_response(self):
        """Get AI response based on transcription"""
        if not self.transcription:
            raise UserError('Please transcribe audio first.')
        
        prompt = f"Based on this CRM message: {self.transcription}\n\nProvide helpful insights or actions."
        self.ai_response = self.get_ai_response(prompt)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'AI response generated',
                'type': 'success',
                'sticky': False,
            }
        }
    
    def button_create_lead_from_voice(self):
        """Create a CRM lead from voice message"""
        if not self.transcription:
            raise UserError('Please transcribe audio first.')
        
        # Use AI to extract lead info from transcription
        extraction_prompt = f"""
        Extract lead information from this voice message. Return JSON format:
        {{"name": "Lead name or company", "description": "Details", "phone": "if available", "email": "if available"}}
        
        Message: {self.transcription}
        """
        
        try:
            ai_extraction = self.get_ai_response(extraction_prompt)
            import json
            lead_data = json.loads(ai_extraction)
        except:
            lead_data = {'name': 'Lead from Voice', 'description': self.transcription}
        
        lead = self.env['crm.lead'].create({
            'name': lead_data.get('name', 'Lead from Voice Message'),
            'description': lead_data.get('description', self.transcription),
            'phone': lead_data.get('phone', ''),
            'email': lead_data.get('email', ''),
            'stage_id': 1,  # New stage
            'team_id': 1,   # Sales team
            'user_id': self.env.user.id,
        })
        
        self.lead_id = lead.id
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'res_id': lead.id,
            'view_mode': 'form',
            'target': 'current',
        }
