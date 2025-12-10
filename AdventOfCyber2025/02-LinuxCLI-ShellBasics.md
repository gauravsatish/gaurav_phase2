Self explanatory.
### Solution for Side Quest 1:
Looking at the file in `Documents/read-me-please.txt`:
```
From: mcskidy
To: whoever finds this

I had a short second when no one was watching. I used it.

I've managed to plant a few clues around the account.
If you can get into the user below and look carefully,
those three little "easter eggs" will combine into a passcode
that unlocks a further message that I encrypted in the
/home/eddi_knapp/Documents/ directory.
I didn't want the wrong eyes to see it.

Access the user account:
username: eddi_knapp
password: S0mething1Sc0ming

There are three hidden easter eggs.
They combine to form the passcode to open my encrypted vault.

Clues (one for each egg):

1)
I ride with your session, not with your chest of files.
Open the little bag your shell carries when you arrive.

2)
The tree shows today; the rings remember yesterday.
Read the ledger’s older pages.

3)
When pixels sleep, their tails sometimes whisper plain words.
Listen to the tail.

Find the fragments, join them in order, and use the resulting passcode
to decrypt the message I left. Be careful — I had to be quick,
and I left only enough to get help.

~ McSkidy
```
The first clue hints at being a part of your session and not a file. It also says to "open the little bag your shell carries when you arrive".
The second part immediately led me to look in `.bashrc` for export statements. These export statements set user defined environment variables that get initialized when you create your terminal session. At the end of the file was this line:
```
export PASSFRAG1="3ast3r"
```
So, we have the first part of our flag. The second clue hints at looking at log files. This one took some time. I searched through `/var/log`, a `wget-log` file present in the home folder, and other random places. Then i noticed the `.secret` and `.secret-git` folders. Since a git repo has a log, I went there first. I checked the `git log`, which showed two commits:
```console
commit e924698378132991ee08f050251242a092c548fd (HEAD -> master)
Author: mcskiddy <mcskiddy@robco.local>
Date:   Thu Oct 9 17:20:11 2025 +0000

    remove sensitive note

commit d12875c8b62e089320880b9b7e41d6765818af3d
Author: McSkidy <mcskiddy@tbfc.local>
Date:   Thu Oct 9 17:19:53 2025 +0000

    add private note
```

Since a "sensitive note" was removed, I ran a `git diff` between the two commits to see what was changed:
```console
git diff d12875c8b62e089320880b9b7e41d6765818af3d
diff --git a/secret_note.txt b/secret_note.txt
deleted file mode 100755
index 060736e..0000000
--- a/secret_note.txt
+++ /dev/null
@@ -1,5 +0,0 @@
-========================================
-Private note from McSkidy
-========================================
-We hid things to buy time.
-PASSFRAG2: -1s-
```
Now, we have the second part.

Looking at the third hint, it talks about pixels and tails, which led me to think about images and the `tail` command. I ran `tree` and saw a whole bunch of images in `Pictures`, so I ran `tail * | grep FRAG`, which yielded no results. Luckily, i had the idea to check for hidden files and noticed a hidden `.easter_egg` file. Running `tail .easter` led me to the password fragment:
```console
tail .easter_egg 
@@@@@@@@@@@@@@@@@@@@@@%#**++=--=====++====----*@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@%*+=-:=++**++**+=-::--*@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@#+=:.+#***=*#=--::-=-=%@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@%%*+-:+%#+++=++=:::==--*%@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@%*+=--*@#++===::::::::=#%@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@%%%##*#%%%####***#*#####%%@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@%%###%%%%%%%%%%##%%##%%@@@@@@@@@@@@

~~ HAPPY EASTER ~~~
PASSFRAG3: c0M1nG
```
Putting it together, the flag is: `3ast3r-1s-c0M1nG`