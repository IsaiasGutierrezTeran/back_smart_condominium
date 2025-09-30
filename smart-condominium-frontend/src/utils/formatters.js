// Smart Condominium - Formateadores
import { formatDate, formatCurrency, capitalize } from './helpers';
import { USER_ROLES, PAYMENT_STATUS, RESERVATION_STATUS, INCIDENT_STATUS, MAINTENANCE_STATUS } from './constants';

// Formatear estado de pago
export const formatPaymentStatus = (status) => {
  const statusMap = {
    [PAYMENT_STATUS.PENDING]: 'Pendiente',
    [PAYMENT_STATUS.PAID]: 'Pagado',
    [PAYMENT_STATUS.OVERDUE]: 'Vencido',
    [PAYMENT_STATUS.CANCELLED]: 'Cancelado',
  };
  
  return statusMap[status] || capitalize(status);
};

// Formatear estado de reserva
export const formatReservationStatus = (status) => {
  const statusMap = {
    [RESERVATION_STATUS.PENDING]: 'Pendiente',
    [RESERVATION_STATUS.APPROVED]: 'Aprobado',
    [RESERVATION_STATUS.REJECTED]: 'Rechazado',
    [RESERVATION_STATUS.CANCELLED]: 'Cancelado',
    [RESERVATION_STATUS.COMPLETED]: 'Completado',
  };
  
  return statusMap[status] || capitalize(status);
};

// Formatear estado de incidente
export const formatIncidentStatus = (status) => {
  const statusMap = {
    [INCIDENT_STATUS.OPEN]: 'Abierto',
    [INCIDENT_STATUS.INVESTIGATING]: 'En Investigación',
    [INCIDENT_STATUS.RESOLVED]: 'Resuelto',
    [INCIDENT_STATUS.CLOSED]: 'Cerrado',
  };
  
  return statusMap[status] || capitalize(status);
};

// Formatear estado de mantenimiento
export const formatMaintenanceStatus = (status) => {
  const statusMap = {
    [MAINTENANCE_STATUS.PENDING]: 'Pendiente',
    [MAINTENANCE_STATUS.IN_PROGRESS]: 'En Progreso',
    [MAINTENANCE_STATUS.COMPLETED]: 'Completado',
    [MAINTENANCE_STATUS.CANCELLED]: 'Cancelado',
  };
  
  return statusMap[status] || capitalize(status);
};

// Formatear rol de usuario
export const formatUserRole = (role) => {
  const roleMap = {
    [USER_ROLES.ADMIN]: 'Administrador',
    [USER_ROLES.RESIDENT]: 'Residente',
    [USER_ROLES.SECURITY]: 'Seguridad',
    [USER_ROLES.MAINTENANCE]: 'Mantenimiento',
  };
  
  return roleMap[role] || capitalize(role);
};

// Formatear prioridad
export const formatPriority = (priority) => {
  const priorityMap = {
    baja: 'Baja',
    media: 'Media',
    alta: 'Alta',
    critica: 'Crítica',
  };
  
  return priorityMap[priority] || capitalize(priority);
};

// Formatear tipo de visitante
export const formatVisitorType = (type) => {
  const typeMap = {
    familiar: 'Familiar',
    amigo: 'Amigo',
    servicio: 'Servicio',
    proveedor: 'Proveedor',
    delivery: 'Delivery',
    otro: 'Otro',
  };
  
  return typeMap[type] || capitalize(type);
};

// Formatear duración en minutos
export const formatDuration = (minutes) => {
  if (!minutes) return '0 min';
  
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  
  if (hours === 0) {
    return `${mins} min`;
  }
  
  if (mins === 0) {
    return `${hours}h`;
  }
  
  return `${hours}h ${mins}min`;
};

// Formatear tamaño de archivo
export const formatFileSize = (bytes) => {
  if (!bytes) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Formatear rango de fechas
export const formatDateRange = (startDate, endDate) => {
  if (!startDate || !endDate) return '';
  
  const start = formatDate(startDate);
  const end = formatDate(endDate);
  
  if (start === end) {
    return start;
  }
  
  return `${start} - ${end}`;
};

// Formatear tiempo relativo
export const formatRelativeTime = (date) => {
  if (!date) return '';
  
  const now = new Date();
  const past = new Date(date);
  const diffInMinutes = Math.floor((now - past) / (1000 * 60));
  
  if (diffInMinutes < 1) {
    return 'Hace un momento';
  }
  
  if (diffInMinutes < 60) {
    return `Hace ${diffInMinutes} min`;
  }
  
  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) {
    return `Hace ${diffInHours}h`;
  }
  
  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays < 7) {
    return `Hace ${diffInDays} días`;
  }
  
  return formatDate(date);
};

// Formatear porcentaje
export const formatPercentage = (value, decimals = 1) => {
  if (value === null || value === undefined) return '0%';
  return `${Number(value).toFixed(decimals)}%`;
};

// Formatear número con separadores de miles
export const formatNumber = (number) => {
  if (number === null || number === undefined) return '0';
  return new Intl.NumberFormat('es-BO').format(number);
};

// Formatear dirección
export const formatAddress = (address) => {
  if (!address) return '';
  
  const parts = [];
  if (address.street) parts.push(address.street);
  if (address.number) parts.push(`#${address.number}`);
  if (address.apartment) parts.push(`Apto. ${address.apartment}`);
  if (address.city) parts.push(address.city);
  
  return parts.join(', ');
};

// Formatear nombre completo
export const formatFullName = (firstName, lastName) => {
  const parts = [];
  if (firstName) parts.push(firstName);
  if (lastName) parts.push(lastName);
  return parts.join(' ');
};

// Formatear resumen de notificación
export const formatNotificationSummary = (notification) => {
  const { tipo, titulo, contenido } = notification;
  
  const typeMap = {
    pago: '💰',
    reserva: '📅',
    seguridad: '🔒',
    mantenimiento: '🔧',
    general: '📢',
  };
  
  const icon = typeMap[tipo] || '📄';
  const summary = contenido ? contenido.substring(0, 100) + '...' : titulo;
  
  return `${icon} ${summary}`;
};