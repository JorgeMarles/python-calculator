from typing import List, Tuple

class Console:


    def read_string(self, msg: str = "") -> str:
        return input(msg)

    def read_int(self, msg: str = "") -> int:
        return int(self.read_string(msg))

    def read_float(self, msg: str = "") -> float:
        return float(self.read_string(msg))

    def print(self, msg: str = "") -> None:
        print(msg)

    def select_from_menu(self, title: str, opts: List[Tuple[str,str]]) -> str:
        self.print(title)
        for opt in opts: 
            self.print(f"{opt[0]}. {opt[1]}")

        while True: 
            selected = self.read_string("Select an option: ")
            for opt in opts:
                if opt[0] == selected: 
                    return selected
                
if __name__=="__main__":
    opts = []
    for i in range(4):
        opts.append((str(i), f"option{i}"))

    c = Console()
    selected = c.select_from_menu("Example menu", opts)
    print(selected)
        
