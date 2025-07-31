import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { catchError, tap } from 'rxjs/operators';
import { throwError } from 'rxjs';

export const httpLoggingInterceptor: HttpInterceptorFn = (req, next) => {
  const startTime = Date.now();
  
  console.log(`HTTP Request: ${req.method} ${req.url}`);
  
  return next(req).pipe(
    tap(() => {
      const elapsedTime = Date.now() - startTime;
      console.log(`HTTP Response: ${req.method} ${req.url} (${elapsedTime}ms)`);
    }),
    catchError((error: HttpErrorResponse) => {
      const elapsedTime = Date.now() - startTime;
      console.error(`HTTP Error: ${req.method} ${req.url} (${elapsedTime}ms)`, error);
      return throwError(() => error);
    })
  );
};
