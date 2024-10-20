INSERT INTO translations (id,	en,	fa) VALUES
	('ERROR 401 DESCRIPTION',	'The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password),	or your browser does not understand how to supply the credentials required.',	'خدمت‌گذار نمی‌تواند تأیید کند که شما مجاز به دسترسی به نشانی درخواست شده هستید. شما یا اعتبارنامه‌های اشتباه را ارائه کرده‌اید (به عنوان مثال یک رمز عبور نامناسب)، یا مرورگر شما نمی‌تواند نحوه تأیید اعتبار مورد نیاز را بفهمد.'),
	('ERROR 401 TITLE',	'Unauthorized',	'غیر مجاز'),
	('ERROR 404 DESCRIPTION',	'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.',	'نشانی درخواستی در خدمت‌گذار یافت نشد. اگر نشانی را به صورت دستی وارد کرده اید، لطفاً نوشته خود را بررسی کرده و دوباره امتحان کنید.'),
	('ERROR 404 TITLE',	'Not Found',	'پیدا نشد'),
	('ERROR 501 DESCRIPTION',	'The server does not support the action requested by the browser.',	'خدمت‌گذار از عملکرد درخواستی مرورگر پشتیبانی نمی‌کند.'),
	('ERROR 501 TITLE',	'Not Implemented',	'پیاده سازی نشده است') ON CONFLICT DO NOTHING;
