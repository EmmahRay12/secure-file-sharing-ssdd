"""
Database Models for Secure File Sharing Application

Defines the SQLAlchemy ORM models for:
- User: Authentication and role management
- SharedFile: Encrypted file metadata
- FilePermission: Access control for shared files
- ActivityLog: Security audit trail
"""

from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from database import db


class User(UserMixin, db.Model):
    """User model with authentication and role-based access control."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'admin' or 'user'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime, nullable=True)
    profile_pic = db.Column(db.String(255), nullable=True)

    # Relationships
    uploaded_files = db.relationship('SharedFile', backref='owner', lazy='dynamic',
                                      foreign_keys='SharedFile.owner_id')
    permissions_received = db.relationship('FilePermission', backref='granted_user',
                                           lazy='dynamic', foreign_keys='FilePermission.user_id')
    activity_logs = db.relationship('ActivityLog', backref='user', lazy='dynamic')

    def set_password(self, password: str):
        """Hash and set the user's password using Werkzeug's secure hashing."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def is_admin(self) -> bool:
        """Check if the user has admin role."""
        return self.role == 'admin'

    def to_dict(self):
        """Return user data as a dictionary (excluding sensitive fields)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None,
            'file_count': self.uploaded_files.count(),
        }


class SharedFile(db.Model):
    """File model storing encrypted file metadata and encryption details."""

    __tablename__ = 'shared_files'

    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False, unique=True)
    file_path = db.Column(db.String(512), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String(100), nullable=False)
    file_hash = db.Column(db.String(64), nullable=False)  # SHA-256 hash for integrity
    encrypted_key = db.Column(db.Text, nullable=False)  # Encrypted per-file key
    nonce = db.Column(db.String(100), nullable=False)  # Base64-encoded nonce

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    permissions = db.relationship('FilePermission', backref='file', lazy='dynamic',
                                   cascade='all, delete-orphan')
    activity_logs = db.relationship('ActivityLog', backref='file', lazy='dynamic')

    def to_dict(self, include_key=False):
        """Return file data as a dictionary."""
        data = {
            'id': self.id,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'file_hash': self.file_hash,
            'owner_id': self.owner_id,
            'owner_name': self.owner.username,
            'uploaded_at': self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': self.is_active,
            'shared_with_count': self.permissions.count(),
        }
        if include_key:
            data['encrypted_key'] = self.encrypted_key
            data['nonce'] = self.nonce
        return data


class FilePermission(db.Model):
    """File sharing permissions model for access control."""

    __tablename__ = 'file_permissions'

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('shared_files.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    can_view = db.Column(db.Boolean, default=True)
    can_download = db.Column(db.Boolean, default=True)
    shared_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shared_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)

    # Ensure a user can only have one permission record per file
    __table_args__ = (db.UniqueConstraint('file_id', 'user_id', name='unique_file_user_permission'),)

    # Relationship for the user who shared the file
    sharer = db.relationship('User', foreign_keys=[shared_by])

    def to_dict(self):
        """Return permission data as a dictionary."""
        return {
            'id': self.id,
            'file_id': self.file_id,
            'file_name': self.file.original_filename,
            'user_id': self.user_id,
            'username': self.granted_user.username,
            'can_view': self.can_view,
            'can_download': self.can_download,
            'shared_by': self.shared_by,
            'sharer_name': self.sharer.username,
            'shared_at': self.shared_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': self.is_active,
        }


class ActivityLog(db.Model):
    """Activity log model for security audit and monitoring."""

    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    file_id = db.Column(db.Integer, db.ForeignKey('shared_files.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Action types for categorization
    ACTION_TYPES = {
        'login': 'User Login',
        'logout': 'User Logout',
        'register': 'User Registration',
        'upload': 'File Upload',
        'download': 'File Download',
        'share': 'File Shared',
        'revoke': 'Access Revoked',
        'delete': 'File Deleted',
        'admin_action': 'Admin Action',
        'password_change': 'Password Changed',
    }

    def to_dict(self):
        """Return activity log data as a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else 'System',
            'file_id': self.file_id,
            'file_name': self.file.original_filename if self.file else None,
            'action': self.action,
            'action_display': self.ACTION_TYPES.get(self.action, self.action),
            'description': self.description,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
