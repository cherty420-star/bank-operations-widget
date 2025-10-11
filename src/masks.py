import logging
from .logger_config import setup_logger

# Настраиваем логгер для модуля masks
logger = setup_logger('masks', 'masks.log', logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.
    
    Args:
        card_number: Номер карты (16 цифр)
    
    Returns:
        Замаскированный номер в формате XXXX XX** **** XXXX
    """
    logger.debug(f"Starting card number masking: {card_number}")
    
    try:
        # Удаляем все нецифровые символы
        digits = ''.join(filter(str.isdigit, card_number))
        
        if len(digits) != 16:
            error_msg = f"Invalid card number length: {len(digits)} digits"
            logger.error(error_msg)
            return card_number
        
        # Форматируем номер карты
        masked_number = f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"
        
        logger.info(f"Card number successfully masked: {masked_number}")
        return masked_number
        
    except Exception as e:
        error_msg = f"Error masking card number '{card_number}': {e}"
        logger.error(error_msg)
        return card_number


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.
    
    Args:
        account_number: Номер счета
    
    Returns:
        Замаскированный номер в формате **XXXX
    """
    logger.debug(f"Starting account number masking: {account_number}")
    
    try:
        # Удаляем все нецифровые символы
        digits = ''.join(filter(str.isdigit, account_number))
        
        if len(digits) < 4:
            error_msg = f"Account number too short: {len(digits)} digits"
            logger.error(error_msg)
            return account_number
        
        # Форматируем номер счета
        masked_number = f"**{digits[-4:]}"
        
        logger.info(f"Account number successfully masked: {masked_number}")
        return masked_number
        
    except Exception as e:
        error_msg = f"Error masking account number '{account_number}': {e}"
        logger.error(error_msg)
        return account_number