// Smart Condominium - Constantes de la aplicación

export const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'https://back-smart-condominium-1.onrender.com';

export const USER_ROLES = {
  ADMIN: 'administrador',
  RESIDENT: 'residente',
  SECURITY: 'seguridad',
  MAINTENANCE: 'mantenimiento',
};

export const PAYMENT_STATUS = {
  PENDING: 'pendiente',
  PAID: 'pagado',
  OVERDUE: 'vencido',
  CANCELLED: 'cancelado',
};

export const RESERVATION_STATUS = {
  PENDING: 'pendiente',
  APPROVED: 'aprobado',
  REJECTED: 'rechazado',
  CANCELLED: 'cancelado',
  COMPLETED: 'completado',
};

export const INCIDENT_STATUS = {
  OPEN: 'abierto',
  INVESTIGATING: 'en_investigacion',
  RESOLVED: 'resuelto',
  CLOSED: 'cerrado',
};

export const MAINTENANCE_STATUS = {
  PENDING: 'pendiente',
  IN_PROGRESS: 'en_progreso',
  COMPLETED: 'completado',
  CANCELLED: 'cancelado',
};

export const VISITOR_STATUS = {
  EXPECTED: 'esperado',
  VISITING: 'en_visita',
  LEFT: 'salio',
  CANCELLED: 'cancelado',
};

export const PRIORITY_LEVELS = {
  LOW: 'baja',
  MEDIUM: 'media',
  HIGH: 'alta',
  CRITICAL: 'critica',
};

export const NOTIFICATION_TYPES = {
  INFO: 'info',
  SUCCESS: 'success',
  WARNING: 'warning',
  ERROR: 'error',
};

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  PROFILE: '/profile',
  FINANCE: '/finance',
  COMMUNICATION: '/communication',
  RESERVATIONS: '/reservations',
  SECURITY: '/security',
  MAINTENANCE: '/maintenance',
};

export const DRAWER_WIDTH = 280;

export const DATE_FORMATS = {
  DISPLAY: 'dd/MM/yyyy',
  API: 'yyyy-MM-dd',
  DATETIME: 'dd/MM/yyyy HH:mm',
  TIME: 'HH:mm',
};

export const FILE_TYPES = {
  IMAGES: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
  DOCUMENTS: ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
};

export const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [5, 10, 25, 50],
};