from app.store import SetCommandOptions


class Set:
    @classmethod
    def response(cls, store, *args):
        set_command_options = cls.get_args(args)
        store.set(set_command_options)
        return f"+OK\r\n"
    
    @classmethod
    def get_args(cls, args):
        key = args[0]
        value = args[1]

        if len(args) == 4 and args[2] == "px":
            expire_time = int(args[3])
            return SetCommandOptions(key, value, expire_time)

        
        return SetCommandOptions(key, value, None)
    