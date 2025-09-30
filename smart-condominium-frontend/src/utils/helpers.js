// Smart Condominium - Funciones auxiliares
import { format, parseISO, isValid } from 'date-fns';
import { es } from 'date-fns/locale';

// Formateo de fechas
export const formatDate = (date, formatStr = 'dd/MM/yyyy') => {
  if (!date) return '';
  
  try {
    const dateObject = typeof date === 'string' ? parseISO(date) : date;
    if (!isValid(dateObject)) return '';
    
    return format(dateObject, formatStr, { locale: es });
  } catch (error) {
    console.error('Error formatting date:', error);
    return '';
  }
};

// Formateo de moneda
export const formatCurrency = (amount) => {
  if (amount === null || amount === undefined) return '$0.00';
  
  return new Intl.NumberFormat('es-BO', {
    style: 'currency',
    currency: 'BOB',
    minimumFractionDigits: 2,
  }).format(amount);
};

// Capitalizar primera letra
export const capitalize = (str) => {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

// Truncar texto
export const truncateText = (text, maxLength = 100) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

// Generar colores aleatorios para avatares
export const stringToColor = (string) => {
  let hash = 0;
  let i;

  for (i = 0; i < string.length; i += 1) {
    hash = string.charCodeAt(i) + ((hash << 5) - hash);
  }

  let color = '#';

  for (i = 0; i < 3; i += 1) {
    const value = (hash >> (i * 8)) & 0xff;
    color += `00${value.toString(16)}`.slice(-2);
  }

  return color;
};

// Generar iniciales para avatares
export const getInitials = (name) => {
  if (!name) return 'U';
  
  const names = name.split(' ');
  if (names.length === 1) {
    return names[0].charAt(0).toUpperCase();
  }
  
  return (names[0].charAt(0) + names[names.length - 1].charAt(0)).toUpperCase();
};

// Validar email
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Validar teléfono boliviano
export const isValidPhone = (phone) => {
  const phoneRegex = /^(\+591|591)?\s?[67]\d{3}\s?\d{4}$/;
  return phoneRegex.test(phone);
};

// Obtener el nombre del día en español
export const getDayName = (date) => {
  const days = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
  return days[date.getDay()];
};

// Obtener el nombre del mes en español
export const getMonthName = (date) => {
  const months = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ];
  return months[date.getMonth()];
};

// Debounce function
export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// Formatear número de teléfono
export const formatPhoneNumber = (phone) => {
  if (!phone) return '';
  
  // Remover espacios y caracteres especiales
  const cleanPhone = phone.replace(/\D/g, '');
  
  // Formatear para números bolivianos
  if (cleanPhone.length === 8) {
    return cleanPhone.replace(/(\d{4})(\d{4})/, '$1-$2');
  }
  
  if (cleanPhone.length === 11 && cleanPhone.startsWith('591')) {
    return cleanPhone.replace(/(\d{3})(\d{4})(\d{4})/, '+$1 $2-$3');
  }
  
  return phone;
};

// Obtener el estado de color según el tipo
export const getStatusColor = (status, type = 'default') => {
  const statusColors = {
    success: '#2E7D32',
    warning: '#F57C00',
    error: '#C62828',
    info: '#1976D2',
    pending: '#9E9E9E',
    approved: '#2E7D32',
    rejected: '#C62828',
    completed: '#2E7D32',
    cancelled: '#9E9E9E',
    paid: '#2E7D32',
    overdue: '#C62828',
    default: '#757575',
  };
  
  return statusColors[status] || statusColors.default;
};

// Generar ID único
export const generateId = () => {
  return Math.random().toString(36).substr(2, 9);
};

// Validar archivo
export const validateFile = (file, allowedTypes, maxSize) => {
  if (!allowedTypes.includes(file.type)) {
    return { valid: false, error: 'Tipo de archivo no permitido' };
  }
  
  if (file.size > maxSize) {
    return { valid: false, error: 'El archivo es demasiado grande' };
  }
  
  return { valid: true };
};

// Obtener extensión de archivo
export const getFileExtension = (filename) => {
  return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2);
};