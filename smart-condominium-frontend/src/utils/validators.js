// Smart Condominium - Validadores
import { isValidEmail, isValidPhone } from './helpers';

// Validadores para formularios
export const validators = {
  // Campos requeridos
  required: (value) => {
    if (!value || (typeof value === 'string' && !value.trim())) {
      return 'Este campo es requerido';
    }
    return null;
  },

  // Email
  email: (value) => {
    if (!value) return null;
    if (!isValidEmail(value)) {
      return 'Ingrese un email válido';
    }
    return null;
  },

  // Contraseña
  password: (value) => {
    if (!value) return null;
    if (value.length < 6) {
      return 'La contraseña debe tener al menos 6 caracteres';
    }
    return null;
  },

  // Confirmar contraseña
  confirmPassword: (value, password) => {
    if (!value) return 'Confirme su contraseña';
    if (value !== password) {
      return 'Las contraseñas no coinciden';
    }
    return null;
  },

  // Teléfono
  phone: (value) => {
    if (!value) return null;
    if (!isValidPhone(value)) {
      return 'Ingrese un número de teléfono válido';
    }
    return null;
  },

  // Número
  number: (value) => {
    if (!value) return null;
    if (isNaN(value)) {
      return 'Ingrese un número válido';
    }
    return null;
  },

  // Número positivo
  positiveNumber: (value) => {
    if (!value) return null;
    if (isNaN(value) || Number(value) <= 0) {
      return 'Ingrese un número positivo';
    }
    return null;
  },

  // Longitud mínima
  minLength: (minLength) => (value) => {
    if (!value) return null;
    if (value.length < minLength) {
      return `Debe tener al menos ${minLength} caracteres`;
    }
    return null;
  },

  // Longitud máxima
  maxLength: (maxLength) => (value) => {
    if (!value) return null;
    if (value.length > maxLength) {
      return `No puede tener más de ${maxLength} caracteres`;
    }
    return null;
  },

  // Fecha
  date: (value) => {
    if (!value) return null;
    const date = new Date(value);
    if (isNaN(date.getTime())) {
      return 'Ingrese una fecha válida';
    }
    return null;
  },

  // Fecha futura
  futureDate: (value) => {
    if (!value) return null;
    const date = new Date(value);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (date < today) {
      return 'La fecha debe ser futura';
    }
    return null;
  },

  // Fecha pasada
  pastDate: (value) => {
    if (!value) return null;
    const date = new Date(value);
    const today = new Date();
    today.setHours(23, 59, 59, 999);
    
    if (date > today) {
      return 'La fecha debe ser anterior a hoy';
    }
    return null;
  },

  // URL
  url: (value) => {
    if (!value) return null;
    try {
      new URL(value);
      return null;
    } catch {
      return 'Ingrese una URL válida';
    }
  },

  // Código postal boliviano
  postalCode: (value) => {
    if (!value) return null;
    const postalCodeRegex = /^\d{4,5}$/;
    if (!postalCodeRegex.test(value)) {
      return 'Ingrese un código postal válido (4-5 dígitos)';
    }
    return null;
  },

  // CI boliviano
  ci: (value) => {
    if (!value) return null;
    const ciRegex = /^\d{7,8}$/;
    if (!ciRegex.test(value)) {
      return 'Ingrese un CI válido (7-8 dígitos)';
    }
    return null;
  },
};

// Función para ejecutar múltiples validadores
export const validate = (value, validatorList = []) => {
  for (const validator of validatorList) {
    const error = typeof validator === 'function' ? validator(value) : validator;
    if (error) {
      return error;
    }
  }
  return null;
};

// Validar formulario completo
export const validateForm = (formData, validationRules) => {
  const errors = {};
  let isValid = true;

  Object.keys(validationRules).forEach((field) => {
    const fieldValidators = validationRules[field];
    const fieldValue = formData[field];
    const error = validate(fieldValue, fieldValidators);
    
    if (error) {
      errors[field] = error;
      isValid = false;
    }
  });

  return { isValid, errors };
};

// Esquemas de validación comunes
export const validationSchemas = {
  login: {
    username: [validators.required],
    password: [validators.required],
  },
  
  register: {
    username: [validators.required, validators.minLength(3)],
    email: [validators.required, validators.email],
    password: [validators.required, validators.password],
    first_name: [validators.required],
    last_name: [validators.required],
  },
  
  profile: {
    first_name: [validators.required],
    last_name: [validators.required],
    email: [validators.required, validators.email],
    phone: [validators.phone],
  },
  
  payment: {
    amount: [validators.required, validators.positiveNumber],
    description: [validators.required, validators.maxLength(255)],
  },
  
  reservation: {
    area_comun: [validators.required],
    fecha_inicio: [validators.required, validators.date, validators.futureDate],
    fecha_fin: [validators.required, validators.date],
    motivo: [validators.required, validators.maxLength(500)],
  },
  
  visitor: {
    nombre: [validators.required, validators.maxLength(100)],
    apellido: [validators.required, validators.maxLength(100)],
    ci: [validators.required, validators.ci],
    telefono: [validators.phone],
    fecha_visita: [validators.required, validators.date],
  },
  
  incident: {
    titulo: [validators.required, validators.maxLength(200)],
    descripcion: [validators.required, validators.maxLength(1000)],
    nivel_gravedad: [validators.required],
  },
  
  maintenance: {
    titulo: [validators.required, validators.maxLength(200)],
    descripcion: [validators.required, validators.maxLength(1000)],
    prioridad: [validators.required],
  },
};