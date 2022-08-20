# workstation-backend

Back-End of Workstation Project

## Run file Linux

```python
pip install -r requirements.txt
cd app
gunicorn -w 2 -b 127.0.0.1:8000 app:app
```

## Todo

- [X] Minor fixes
- [X] New way to send email
- [X] Endpoints update user info
- [X] Process input data
- [X] Create sql static data boxes
- [x] Recreate box get
- [ ] Recreate Schedule
- [ ] Deploy

## References

- [Email html template](https://beefree.io/templates/)
